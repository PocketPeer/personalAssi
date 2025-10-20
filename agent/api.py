from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import time

from agent.morning_brief.service import MorningBriefService
from agent.integrations.notifier import TeamsWebhookNotifier
from agent.skills.loader import SkillLoader
from agent.skills.renderer import SkillsRenderer
from agent.finance.config import JsonPortfolioStore, Portfolio, Position
from agent.finance.monitor import PortfolioMonitor

app = FastAPI(title="Day Agent API")

@app.get("/callback/approve")
def approve(item: str):
    return JSONResponse({"status": "approved", "item": item, "ts": int(time.time())})

@app.get("/callback/decline")
def decline(item: str):
    return JSONResponse({"status": "declined", "item": item, "ts": int(time.time())})


def get_morning_brief_service() -> MorningBriefService:
    loader = SkillLoader()
    renderer = SkillsRenderer(loader)
    notifier = TeamsWebhookNotifier("")  # placeholder; URL is provided at send time
    return MorningBriefService(renderer=renderer, notifier=notifier)


def get_portfolio_store() -> JsonPortfolioStore:
    return JsonPortfolioStore()


def get_portfolio_monitor() -> PortfolioMonitor:
    # For real use, inject a real market data provider and notifier
    from agent.finance.market_data import MarketDataProvider, Quote  # type: ignore
    class DummyProvider:  # placeholder provider
        def get_quote(self, symbol: str):
            return Quote(symbol=symbol, price=0.0, currency="USD")
    return PortfolioMonitor(provider=DummyProvider(), notifier=TeamsWebhookNotifier("") )


class BriefPreviewQuery(BaseModel):
    agenda: str
    emails: str
    nudges: str


@app.get("/brief/preview")
def brief_preview(agenda: str, emails: str, nudges: str):
    svc = get_morning_brief_service()
    text = svc.build_brief({"agenda": agenda, "emails": emails, "nudges": nudges})
    return {"text": text}


class BriefSendBody(BaseModel):
    webhook_url: str
    agenda: str
    emails: str
    nudges: str


@app.post("/brief/send")
def brief_send(body: BriefSendBody):
    svc = get_morning_brief_service()
    text = svc.build_brief({"agenda": body.agenda, "emails": body.emails, "nudges": body.nudges})
    ok = svc.send_brief(body.webhook_url, text)
    return {"ok": ok}


class PortfolioBody(BaseModel):
    positions: list[dict]


@app.post("/portfolio/{name}")
def portfolio_save(name: str, body: PortfolioBody):
    store = get_portfolio_store()
    positions = [Position(**p) for p in body.positions]
    store.save(name, Portfolio(positions=positions))
    return {"ok": True}


@app.get("/portfolio/{name}")
def portfolio_load(name: str):
    store = get_portfolio_store()
    p = store.load(name)
    return {"positions": [{"symbol": pos.symbol, "shares": pos.shares} for pos in p.positions]}


class CheckRulesBody(BaseModel):
    rules: list[dict] = []


@app.post("/portfolio/{name}/check")
def portfolio_check(name: str, body: CheckRulesBody):
    store = get_portfolio_store()
    monitor = get_portfolio_monitor()
    p = store.load(name)
    # Convert rules if any; for now, pass as empty or raw dicts ignored by dummy monitor
    _ = body.rules
    monitor.check(p, [])
    return {"ok": True}
