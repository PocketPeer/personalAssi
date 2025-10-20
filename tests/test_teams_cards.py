from agent.integrations.teams_cards import build_approval_card


def test_build_approval_card_shape():
    card = build_approval_card("42", "https://example.com/approve?item=42", "https://example.com/decline?item=42")
    assert card["type"] == "message"
    assert isinstance(card["attachments"], list) and card["attachments"], "attachments missing"
    att = card["attachments"][0]
    assert att["contentType"] == "application/vnd.microsoft.card.adaptive"
    content = att["content"]
    assert content["type"] == "AdaptiveCard"
    assert any(a.get("title", "").startswith("✅") for a in content["actions"])  # approve action present
    assert any(a.get("title", "").startswith("❌") for a in content["actions"])  # decline action present
