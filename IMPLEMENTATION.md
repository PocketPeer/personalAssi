# Implementation Guide (for Builder AI / Dev Team)

- Open `agent_implementation_spec.json` for the full machine-readable spec.
- Create/complete modules according to the specified directory layout.
- Wire Microsoft Graph (calendar/mail/drive), Teams webhook, and Azure Speech.
- Respect autonomy tiers and route TIER2 via Teams approvals.
- Start with read-only; add actions gradually.

Quickstart:
```
pip install -r infra/requirements.txt
cp .env.example .env  # add keys
```