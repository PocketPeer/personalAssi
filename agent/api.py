from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import time

from agent.morning_brief.service import MorningBriefService
from agent.integrations.notifier import TeamsWebhookNotifier
from agent.skills.loader import SkillLoader
from agent.skills.renderer import SkillsRenderer

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
