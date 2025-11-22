from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from app.database.config import Base, engine
from app.domain.user import User
from app.domain.portfolio import Portfolio
from app.domain.investment import Investment
from app.domain.security import Security  
from app.domain.transaction import TradeTransaction
Base.metadata.create_all(bind=engine)

console = Console()

def main_menu(user):
    """Display the main menu after successful login."""
    while True:
        console.clear()

        console.print(Panel.fit(
            f"[bold cyan]Main Menu — Logged in as {user.username}[/bold cyan]",
            border_style="cyan"
        ))
        console.print("[1] Manage Users")
        console.print("[2] Manage Portfolios")
        console.print("[3] Marketplace")
        console.print("[4] Logout\n")

        choice = Prompt.ask(
            "[bold yellow]Enter your choice[/bold yellow]",
            choices=["1", "2", "3", "4"]
        )

        if choice == "1":
            from app.cli.manage_users_menu import manage_users_menu
            manage_users_menu(user)

        elif choice == "2":
            from app.cli.manage_portfolios_menu import manage_portfolios_menu
            manage_portfolios_menu(user)

        elif choice == "3":
            from app.cli.marketplace_menu import marketplace_menu
            marketplace_menu(user)

        elif choice == "4":
            console.print("\n[bold red]Logging out... Returning to Login Menu.[/bold red]\n")
            from app.cli.login_menu import login_menu
            login_menu()
            return