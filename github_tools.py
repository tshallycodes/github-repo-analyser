import requests
import base64

GITHUB_API = "https://api.github.com"

def parse_repo_url(url: str) -> tuple[str, str]:
    """Extract owner and repo name from GitHub URL."""
    url = url.rstrip("/").replace("https://github.com/", "") # 
    parts = url.split("/")
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL. Expected: https://github.com/owner/repo")
    return parts[0], parts[1]


def get_repo_info(owner: str, repo: str) -> dict:
    """Fetch basic repo metadata."""
    response = requests.get(f"{GITHUB_API}/repos/{owner}/{repo}")
    response.raise_for_status()
    data = response.json()
    return {
        "name": data.get("name"),
        "description": data.get("description"),
        "language": data.get("language"),
        "stars": data.get("stargazers_count"),
        "forks": data.get("forks_count"),
        "topics": data.get("topics", []),
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
        "size_kb": data.get("size"),
    }


def get_file_tree(owner: str, repo: str, max_files: int = 50) -> list[str]:
    """Fetch the full file tree of the repo."""
    response = requests.get(
        f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/HEAD",
        params={"recursive": "1"}
    )
    response.raise_for_status()
    tree = response.json().get("tree", [])
    files = [
        item["path"] for item in tree
        if item["type"] == "blob"
    ]
    return files[:max_files]


def get_file_content(owner: str, repo: str, path: str, max_chars: int = 3000) -> str:
    """Fetch and decode a file's content from the repo."""
    response = requests.get(f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}")
    if response.status_code != 200:
        return ""
    data = response.json()
    if data.get("encoding") == "base64":
        try:
            content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
            return content[:max_chars]
        except Exception:
            return ""
    return ""


def pick_key_files(file_list: list[str]) -> list[str]:
    """Select the most informative files to read."""
    priority = []
    rest = []

    priority_names = {
        "readme.md", "readme.txt", "readme",
        "main.py", "app.py", "run.py", "index.py",
        "train.py", "predict.py", "inference.py",
        "requirements.txt", "setup.py", "pyproject.toml",
        "dockerfile", "docker-compose.yml",
        "config.py", "config.yaml", "config.json",
        ".env.example"
    }

    for f in file_list:
        filename = f.split("/")[-1].lower()
        if filename in priority_names:
            priority.append(f)
        else:
            rest.append(f)

    # Add a sample of remaining .py files
    py_files = [f for f in rest if f.endswith(".py")][:5]
    return priority + py_files