import anthropic
import os
from dotenv import load_dotenv
from github_tools import (
    parse_repo_url,
    get_repo_info,
    get_file_tree,
    get_file_content,
    pick_key_files,
)

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_KEY"))


def build_context(owner: str, repo: str) -> str:
    """Gather all repo data into a single context string for the agent."""
    print("  → Fetching repo metadata...")
    info = get_repo_info(owner, repo)

    print("  → Fetching file tree...")
    all_files = get_file_tree(owner, repo)
    key_files = pick_key_files(all_files)

    print(f"  → Reading {len(key_files)} key files...")
    file_contents = []
    for path in key_files:
        content = get_file_content(owner, repo, path)
        if content:
            file_contents.append(f"### FILE: {path}\n```\n{content}\n```")

    context = f"""
REPO METADATA:
- Name: {info['name']}
- Description: {info['description']}
- Primary Language: {info['language']}
- Stars: {info['stars']} | Forks: {info['forks']}
- Topics: {', '.join(info['topics']) or 'None'}
- Size: {info['size_kb']} KB
- Last Updated: {info['updated_at']}

ALL FILES IN REPO:
{chr(10).join(all_files)}

KEY FILE CONTENTS:
{chr(10).join(file_contents)}
"""
    return context.strip()


def analyse_repo(url: str) -> str:
    """Main agent function — fetch repo data and generate analysis."""
    print(f"\n🔍 Analysing: {url}")

    owner, repo = parse_repo_url(url)
    context = build_context(owner, repo)

    print("  → Running AI analysis...")

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2000,
        system="""You are a senior software engineer performing a technical code review.
Analyse the provided GitHub repository and produce a clear, structured technical report.
Be specific, practical, and honest. If code quality is poor, say so.""",
        messages=[
            {
                "role": "user",
                "content": f"""Analyse this GitHub repository and write a technical summary report in markdown.

{context}

Your report must include these sections:
1. **Overview** — What this project does in plain English
2. **Tech Stack** — Languages, frameworks, libraries detected
3. **Architecture** — How the code is structured and organised
4. **Key Features** — What the system actually does
5. **Code Quality** — Honest assessment: strengths and weaknesses
6. **Potential Improvements** — 3-5 concrete suggestions
7. **Verdict** — One paragraph summary for someone deciding whether to use or contribute to this repo
"""
            }
        ]
    )

    return response.content[0].text
