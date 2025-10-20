from typing import Dict, Any

def build_approval_card(item_id: str, approve_url: str, decline_url: str) -> Dict[str, Any]:
    return {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.5",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": "Approval required",
                            "weight": "Bolder",
                            "size": "Medium"
                        },
                        {
                            "type": "TextBlock",
                            "text": f"Item: {item_id}",
                            "wrap": True
                        }
                    ],
                    "actions": [
                        {
                            "type": "Action.OpenUrl",
                            "title": "✅ Genehmigen",
                            "url": approve_url
                        },
                        {
                            "type": "Action.OpenUrl",
                            "title": "❌ Ablehnen",
                            "url": decline_url
                        }
                    ]
                }
            }
        ]
    }
