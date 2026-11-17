# AI Feedback Analyzer

A Python command-line tool that reads customer feedback (one entry per line) and uses the Google Gemini API to classify each entry as **positive**, **neutral** or **negative** and write a one-line summary. Results are saved as JSON and CSV, and a short sentiment report is printed.

## Features
- Calls an LLM API with a structured prompt and validates the JSON reply
- Strips markdown code fences and rejects invalid sentiment labels
- Retries failed requests; a failed entry is recorded without stopping the run
- Exports results to `results.json` and `results.csv`
- Unit tests with mocked API calls (no API key needed to run them)

## Setup
1. Install Python 3.9 or newer.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Get a free API key from [Google AI Studio](https://aistudio.google.com/) and set it:
   ```bash
   export GEMINI_API_KEY="your-key"        # Windows PowerShell: $env:GEMINI_API_KEY="your-key"
   ```
   Never commit your key to GitHub.

## Usage
```bash
python feedback_analyzer.py sample_feedback.txt
python feedback_analyzer.py my_feedback.txt --out my_results
python feedback_analyzer.py sample_feedback.txt --model gemini-2.5-flash
```
The model can also be set with the `GEMINI_MODEL` environment variable. If a model name stops working, check the current names in the Gemini API docs.

## Output
`results.json` and `results.csv` contain, for each entry: `text`, `sentiment`, `summary` and `error` (empty on success).

## Run the tests
```bash
python -m pytest -v
```

## Project structure
- `feedback_analyzer.py`: prompt building, API call, response parsing, retries, file output, CLI
- `tests/test_feedback_analyzer.py`: unit tests with mocked API calls
- `sample_feedback.txt`: example input

## Possible improvements
- Process entries in batches to reduce API calls
- Add topic extraction (delivery, pricing, support)
- Add a simple chart of the sentiment counts

## Tech
Python, Requests, Google Gemini API, Pytest
