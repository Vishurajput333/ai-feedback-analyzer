"""AI Feedback Analyzer.

Reads customer feedback (one entry per line), asks an LLM API (Google Gemini)
to classify the sentiment and write a one-line summary for each entry, then
saves the results as JSON and CSV and prints a short report.
"""
import argparse
import csv
import json
import os
import re
import sys
import time

import requests

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
VALID_SENTIMENTS = {"positive", "neutral", "negative"}

PROMPT_TEMPLATE = (
    "You analyze customer feedback. Read the feedback below and reply with ONLY "
    'a JSON object in this exact format: {{"sentiment": "positive|neutral|negative", '
    '"summary": "one short sentence"}}.\n\nFeedback: {text}'
)


def build_prompt(text):
    """Return the prompt sent to the model for one feedback entry."""
    return PROMPT_TEMPLATE.format(text=text)


def call_llm(prompt, api_key, model=DEFAULT_MODEL, timeout=30):
    """Send a prompt to the Gemini API and return the model's text reply."""
    response = requests.post(
        API_URL.format(model=model),
        headers={"x-goog-api-key": api_key, "Content-Type": "application/json"},
        json={"contents": [{"parts": [{"text": prompt}]}]},
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError) as exc:
        raise ValueError("Unexpected API response format") from exc


def parse_response(raw):
    """Turn the model's text reply into a validated {sentiment, summary} dict."""
    cleaned = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
    data = json.loads(cleaned)
    sentiment = str(data.get("sentiment", "")).strip().lower()
    if sentiment not in VALID_SENTIMENTS:
        raise ValueError(f"Invalid sentiment: {sentiment!r}")
    return {"sentiment": sentiment, "summary": str(data.get("summary", "")).strip()}


def analyze_text(text, api_key, model=DEFAULT_MODEL, caller=call_llm, retries=2):
    """Analyze one feedback entry. Retries on failure, never raises."""
    last_error = None
    for attempt in range(retries + 1):
        try:
            reply = caller(build_prompt(text), api_key, model)
            return {"text": text, **parse_response(reply), "error": ""}
        except Exception as exc:  # network, API or parsing problem
            last_error = str(exc)
            if attempt < retries:
                time.sleep(1)
    return {"text": text, "sentiment": "", "summary": "", "error": last_error}


def load_feedback(path):
    """Read feedback entries from a text file, skipping blank lines."""
    with open(path, encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def save_results(results, json_path, csv_path):
    """Write results to a JSON file and a CSV file."""
    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2, ensure_ascii=False)
    with open(csv_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["text", "sentiment", "summary", "error"])
        writer.writeheader()
        writer.writerows(results)


def count_sentiments(results):
    """Count how many entries fall into each sentiment (and how many failed)."""
    counts = {"positive": 0, "neutral": 0, "negative": 0, "failed": 0}
    for item in results:
        if item["error"]:
            counts["failed"] += 1
        else:
            counts[item["sentiment"]] += 1
    return counts


def main(argv=None):
    parser = argparse.ArgumentParser(description="Classify and summarize feedback with an LLM.")
    parser.add_argument("input", help="Text file with one feedback entry per line")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Gemini model name")
    parser.add_argument("--out", default="results", help="Output file prefix (default: results)")
    args = parser.parse_args(argv)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        sys.exit("Set the GEMINI_API_KEY environment variable first (see README).")

    entries = load_feedback(args.input)
    if not entries:
        sys.exit("The input file has no feedback entries.")

    results = []
    for number, text in enumerate(entries, start=1):
        print(f"Analyzing {number}/{len(entries)}...")
        results.append(analyze_text(text, api_key, args.model))

    save_results(results, f"{args.out}.json", f"{args.out}.csv")
    counts = count_sentiments(results)
    print("\nSentiment report")
    for label, value in counts.items():
        print(f"  {label:<9}{value}")
    print(f"\nSaved {args.out}.json and {args.out}.csv")


if __name__ == "__main__":
    main()
