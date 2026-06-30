import json
from typing import Any, Dict, Optional

try:
    from anthropic import Anthropic
except ImportError:  # pragma: no cover
    Anthropic = None  # type: ignore[assignment]


SYSTEM_PROMPT = (
    "You analyze inbound sales leads for service businesses. "
    "Return concise JSON with keys: summary, urgency, intent, next_action."
)


def _build_prompt(lead: Dict[str, Any]) -> str:
    lead_payload = json.dumps(lead, ensure_ascii=True)
    return (
        "Analyze this lead and return only JSON with keys "
        "summary, urgency, intent, next_action.\n"
        f"Lead: {lead_payload}"
    )


def _safe_parse_json(text: str) -> Dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Claude did not return valid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("Claude response JSON must be an object.")

    return {
        "summary": str(data.get("summary", "")),
        "urgency": str(data.get("urgency", "unknown")),
        "intent": str(data.get("intent", "unknown")),
        "next_action": str(data.get("next_action", "follow_up")),
    }


def extract_lead_insights(
    lead: Dict[str, Any],
    model: str,
    api_key: Optional[str],
    dry_run: bool = False,
) -> Dict[str, Any]:
    if dry_run:
        return {
            "summary": f"Lead {lead.get('name')} from {lead.get('source')}.",
            "urgency": "medium",
            "intent": "requested service quote",
            "next_action": "call within 60 seconds",
        }

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is required when dry_run is False.")
    if Anthropic is None:
        raise ImportError(
            "anthropic package is not installed. Run: pip install -r requirements.txt"
        )

    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=250,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": _build_prompt(lead),
            }
        ],
    )

    text_blocks = []
    for block in response.content:
        if getattr(block, "type", "") == "text":
            text_blocks.append(block.text)

    response_text = "\n".join(text_blocks).strip()
    if not response_text:
        raise ValueError("Claude returned empty response text.")

    return _safe_parse_json(response_text)
