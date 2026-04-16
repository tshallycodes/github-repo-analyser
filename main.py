import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
from datetime import datetime
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from analyser import analyse_repo

console = Console()


def save_report(url: str, report: str):
    """Save the report to a markdown file."""
    repo_name = url.rstrip("/").split("/")[-1]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{repo_name}_{timestamp}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# GitHub Repo Analysis: {repo_name}\n")
        f.write(f"> Source: {url}\n")
        f.write(f"> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(report)

    return filename


def main():
    console.print(Panel.fit(
        "[bold cyan]GitHub Repo Analyser[/bold cyan]\n[dim]Powered by Claude[/dim]",
        border_style="cyan"
    ))

    # Get URL from argument or prompt
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = Prompt.ask("\n[cyan]Enter GitHub repo URL[/cyan]")

    if not url.startswith("https://github.com/"):
        console.print("[red]Error: Please provide a valid GitHub URL[/red]")
        sys.exit(1)

    try:
        report = analyse_repo(url)

        console.print("\n")
        console.print(Markdown(report))

        # Save report
        filename = save_report(url, report)
        console.print(f"\n[green]✓ Report saved to:[/green] [bold]{filename}[/bold]")

    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()