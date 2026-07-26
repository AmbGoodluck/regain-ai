import json

import httpx
import pytest
from anthropic import APIError, RateLimitError

import extractor
from extractor import _needs_review, _parse_json_response, extract_leads


# --- _parse_json_response ---------------------------------------------------

def test_parse_json_response_extracts_clean_json():
    text = '{"full_name": "Dana Lee", "email": "dana@example.com"}'
    assert _parse_json_response(text) == {"full_name": "Dana Lee", "email": "dana@example.com"}


def test_parse_json_response_strips_markdown_fences():
    text = '```json\n{"full_name": "Dana Lee"}\n```'
    assert _parse_json_response(text) == {"full_name": "Dana Lee"}


def test_parse_json_response_raises_when_no_json_object_present():
    with pytest.raises(ValueError):
        _parse_json_response("no json here")


# --- _needs_review -----------------------------------------------------------

def test_needs_review_false_for_valid_email_and_phone():
    assert _needs_review("dana@example.com", "415-555-0101") is False


def test_needs_review_true_for_malformed_email():
    assert _needs_review("not-an-email", "415-555-0101") is True


def test_needs_review_true_for_short_phone():
    assert _needs_review("dana@example.com", "123") is True


def test_needs_review_true_when_fields_missing():
    assert _needs_review("", "") is True


# --- extract_leads (client mocked, no real API calls) ------------------------

class FakeClient:
    """Stand-in for anthropic.Anthropic that returns canned responses in order."""

    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = 0
        self.messages = self

    def create(self, **kwargs):
        self.calls += 1
        result = self._responses.pop(0)
        if isinstance(result, Exception):
            raise result
        return _fake_response(result)


def _fake_response(text):
    class _Content:
        def __init__(self, text):
            self.text = text

    class _Response:
        def __init__(self, text):
            self.content = [_Content(text)]

    return _Response(text)


def _rate_limit_error():
    req = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
    return RateLimitError("rate limited", response=httpx.Response(429, request=req), body=None)


def _api_error():
    req = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
    return APIError("server error", request=req, body=None)


def test_extract_leads_returns_structured_lead_on_success(monkeypatch):
    client = FakeClient([json.dumps({
        "full_name": "Marcus Johnson",
        "email": "marcus@example.com",
        "phone": "415-555-0101",
        "service_requested": "roof repair",
        "urgency": "high",
        "preferred_contact_time": "",
    })])
    monkeypatch.setattr(extractor, "_build_client", lambda: client)

    leads, success_count, error_count = extract_leads([{"name": "Marcus Johnson"}])

    assert success_count == 1
    assert error_count == 0
    assert leads[0]["full_name"] == "Marcus Johnson"
    assert leads[0]["source_row"] == 1
    assert leads[0]["needs_review"] is False


def test_extract_leads_flags_malformed_contact_info(monkeypatch):
    client = FakeClient([json.dumps({
        "full_name": "Dana Lee",
        "email": "not-an-email",
        "phone": "",
        "service_requested": "hvac",
        "urgency": "medium",
        "preferred_contact_time": "",
    })])
    monkeypatch.setattr(extractor, "_build_client", lambda: client)

    leads, success_count, error_count = extract_leads([{"name": "Dana Lee"}])

    assert success_count == 1
    assert leads[0]["needs_review"] is True


def test_extract_leads_retries_once_on_generic_error_then_succeeds(monkeypatch):
    good_response = json.dumps({"full_name": "Priya Patel", "email": "priya@example.com", "phone": "415-555-0133"})
    client = FakeClient([_api_error(), good_response])
    monkeypatch.setattr(extractor, "_build_client", lambda: client)

    leads, success_count, error_count = extract_leads([{"name": "Priya Patel"}])

    assert client.calls == 2
    assert success_count == 1
    assert error_count == 0


def test_extract_leads_logs_and_skips_row_after_second_failure(monkeypatch):
    client = FakeClient([_api_error(), _api_error()])
    monkeypatch.setattr(extractor, "_build_client", lambda: client)

    leads, success_count, error_count = extract_leads([{"name": "Bad Row"}])

    assert leads == []
    assert success_count == 0
    assert error_count == 1


def test_extract_leads_retries_rate_limit_with_backoff(monkeypatch):
    monkeypatch.setattr(extractor.time, "sleep", lambda _seconds: None)
    good_response = json.dumps({"full_name": "Marcus Johnson", "email": "marcus@example.com", "phone": "415-555-0101"})
    client = FakeClient([_rate_limit_error(), _rate_limit_error(), good_response])
    monkeypatch.setattr(extractor, "_build_client", lambda: client)

    leads, success_count, error_count = extract_leads([{"name": "Marcus Johnson"}])

    assert client.calls == 3
    assert success_count == 1


def test_extract_leads_continues_to_next_row_after_a_failed_row(monkeypatch):
    good_response = json.dumps({"full_name": "Dana Lee", "email": "dana@example.com", "phone": "415-555-0199"})
    client = FakeClient([_api_error(), _api_error(), good_response])
    monkeypatch.setattr(extractor, "_build_client", lambda: client)

    leads, success_count, error_count = extract_leads([{"name": "Bad Row"}, {"name": "Dana Lee"}])

    assert error_count == 1
    assert success_count == 1
    assert leads[0]["source_row"] == 2


def test_build_client_raises_clear_error_without_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(extractor, "load_dotenv", lambda: None)

    with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
        extractor._build_client()
