# AI Feedback Analyzer

An AI-powered Python application that automates customer feedback analysis using the **Google Gemini API**. The application reads customer feedback from a text file, classifies the sentiment, generates concise summaries, validates AI responses, and exports structured results in both **JSON** and **CSV** formats.

---

## Features

- 🤖 Integrates with the **Google Gemini API** for sentiment analysis and summarization
- 📄 Reads multiple customer feedback entries from a text file
- 📊 Classifies feedback as **Positive**, **Neutral**, or **Negative**
- 📝 Generates concise AI-powered summaries
- ✅ Validates JSON responses before processing
- 🔄 Automatically retries failed API requests
- 💾 Exports results to both **JSON** and **CSV**
- 🧪 Includes unit tests with mocked API responses using **Pytest**
- ⚠️ Handles API and parsing errors without stopping the entire process

---

## Workflow

```text
Customer Feedback File
          │
          ▼
 Read Each Feedback Entry
          │
          ▼
 Build Prompt for Gemini API
          │
          ▼
  Google Gemini API
          │
          ▼
 Validate JSON Response
          │
          ▼
Generate Summary & Sentiment
          │
          ▼
 Export Results (JSON & CSV)
```

---

## Project Structure

```text
ai-feedback-analyzer/
│
├── feedback_analyzer.py          # Main application
├── requirements.txt              # Python dependencies
├── sample_feedback.txt           # Sample input
├── README.md
├── .gitignore
│
└── tests/
    └── test_feedback_analyzer.py # Unit tests
```

---

## Technologies Used

- Python 3.9+
- Google Gemini API
- Requests
- JSON
- CSV
- Pytest

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Vishurajput333/ai-feedback-analyzer.git
cd ai-feedback-analyzer
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Configure the API Key

Generate a free API key from **Google AI Studio**.

Set the environment variable:

### Windows PowerShell

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

### Linux / macOS

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

> **Note:** Never commit your API key to GitHub.

---

## Usage

Analyze the sample feedback:

```bash
python feedback_analyzer.py sample_feedback.txt
```

Analyze your own file:

```bash
python feedback_analyzer.py my_feedback.txt
```

Specify an output file name:

```bash
python feedback_analyzer.py my_feedback.txt --out results
```

Specify a Gemini model:

```bash
python feedback_analyzer.py sample_feedback.txt --model gemini-2.5-flash
```

---

## Output

The application generates:

- `results.json`
- `results.csv`

Each record contains:

| Field | Description |
|-------|-------------|
| text | Original customer feedback |
| sentiment | Positive, Neutral, or Negative |
| summary | AI-generated summary |
| error | Error message (if processing fails) |

---

## Testing

Run all unit tests:

```bash
python -m pytest -v
```

The project uses mocked Gemini API responses, allowing tests to run without an API key or internet connection.

---

## Skills Demonstrated

This project demonstrates practical AI engineering skills including:

- LLM API Integration
- Prompt Engineering
- AI-powered Text Processing
- JSON Validation
- Error Handling
- Retry Logic
- Automation Workflows
- File Processing
- Unit Testing
- Python CLI Development

---

## Future Improvements

- Build a FastAPI REST API
- Develop a web interface using Flask or Streamlit
- Support asynchronous API requests
- Batch feedback processing for improved performance
- Interactive dashboard for sentiment visualization
- Topic extraction (pricing, delivery, customer support)
- Docker support for easy deployment

---

## Why This Project?

This project was built to demonstrate practical AI application development using modern Large Language Models. It showcases how an LLM can be integrated into a reliable automation workflow with validation, retries, structured outputs, and testing—skills commonly required in AI Engineering, Machine Learning, and Generative AI roles.

---

## Author

**Vishwajeet Singh Manhas**

- GitHub: https://github.com/Vishurajput333

If you found this project useful, consider giving it a ⭐ on GitHub.
