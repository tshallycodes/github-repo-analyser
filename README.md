# 🔍 GitHub Repo Analyser

An AI agent that analyses any public GitHub repository and generates a detailed technical report — architecture, code quality, stack, and improvement suggestions.

Powered by Claude (Anthropic).

## Features

- Fetches repo metadata, file tree, and key file contents via GitHub API
- Intelligently selects the most informative files to read
- Generates a structured markdown report with AI analysis
- Saves report to a local `.md` file
- Clean terminal output with syntax highlighting

## Setup

```bash
# Clone the repo
git clone https://github.com/tshallycodes/github-repo-analyser
cd github-repo-analyser

# Install dependencies
pip install -r requirements.txt

# Set your Anthropic API key
export ANTHROPIC_API_KEY=your_key_here   # Mac/Linux
$env:ANTHROPIC_API_KEY="your_key_here"  # Windows PowerShell
```

## Usage

```bash
# Pass URL directly
python main.py https://github.com/owner/repo

# Or run interactively
python main.py
```

## Example Output

```
🔍 Analysing: https://github.com/owner/repo
  → Fetching repo metadata...
  → Fetching file tree...
  → Reading 8 key files...
  → Running AI analysis...

# Overview
This project is a...

✓ Report saved to: report_repo_20240416_143022.md
```

## Stack

- Python 3.10+
- [Anthropic SDK](https://github.com/anthropic-ai/anthropic-sdk-python)
- GitHub REST API (no auth required for public repos)
- [Rich](https://github.com/Textualize/rich) for terminal output
