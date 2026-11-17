import json
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import feedback_analyzer as fa


def test_parse_plain_json():
    out = fa.parse_response('{"sentiment": "Positive", "summary": "Loved it"}')
    assert out == {"sentiment": "positive", "summary": "Loved it"}


def test_parse_fenced_json():
    raw = '```json\n{"sentiment": "negative", "summary": "Too slow"}\n```'
    assert fa.parse_response(raw)["sentiment"] == "negative"


def test_parse_invalid_sentiment():
    with pytest.raises(ValueError):
        fa.parse_response('{"sentiment": "happy", "summary": "x"}')


def test_parse_not_json():
    with pytest.raises(json.JSONDecodeError):
        fa.parse_response("not json")


def test_analyze_text_success():
    caller = lambda prompt, key, model: '{"sentiment": "neutral", "summary": "Okay"}'
    result = fa.analyze_text("It was fine", "key", caller=caller)
    assert result["sentiment"] == "neutral" and result["error"] == ""


def test_analyze_text_retries_then_fails():
    calls = []

    def bad_caller(prompt, key, model):
        calls.append(1)
        raise RuntimeError("API down")

    with patch("feedback_analyzer.time.sleep"):
        result = fa.analyze_text("x", "key", caller=bad_caller, retries=2)
    assert len(calls) == 3 and result["error"] == "API down"


def test_call_llm_reads_reply():
    fake = MagicMock()
    fake.json.return_value = {"candidates": [{"content": {"parts": [{"text": "hi"}]}}]}
    with patch("feedback_analyzer.requests.post", return_value=fake) as post:
        assert fa.call_llm("prompt", "key") == "hi"
    assert post.call_args.kwargs["headers"]["x-goog-api-key"] == "key"


def test_call_llm_bad_format():
    fake = MagicMock()
    fake.json.return_value = {"unexpected": True}
    with patch("feedback_analyzer.requests.post", return_value=fake):
        with pytest.raises(ValueError):
            fa.call_llm("prompt", "key")


def test_load_feedback_skips_blanks(tmp_path):
    path = tmp_path / "in.txt"
    path.write_text("one\n\n  two  \n", encoding="utf-8")
    assert fa.load_feedback(path) == ["one", "two"]


def test_count_sentiments():
    results = [
        {"sentiment": "positive", "error": ""},
        {"sentiment": "negative", "error": ""},
        {"sentiment": "", "error": "boom"},
    ]
    assert fa.count_sentiments(results) == {"positive": 1, "neutral": 0, "negative": 1, "failed": 1}


def test_save_results(tmp_path):
    rows = [{"text": "a", "sentiment": "positive", "summary": "s", "error": ""}]
    fa.save_results(rows, tmp_path / "r.json", tmp_path / "r.csv")
    assert json.loads((tmp_path / "r.json").read_text())[0]["text"] == "a"
    assert "positive" in (tmp_path / "r.csv").read_text()
