from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
import db

console = Console()

def main_menu():
    """Display the main menu after successful login."""
    while True:
        console.clear()
        user = db.logged_in_user

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

        # 1. Manage Users
        if choice == "1":
            if user.username != "eyared":
                console.print(
                    "[red]Access denied — only the admin can manage users.[/red]"
                )
                input("Press Enter to return to Main Menu...")
            else:
                from app.cli.manage_users_menu import manage_users_menu
                manage_users_menu()

        # 2. Manage Portfolios
        elif choice == "2":
            from app.cli.manage_portfolios_menu import manage_portfolios_menu
            manage_portfolios_menu()

        #  3. Marketplace
        elif choice == "3":
            from app.cli.marketplace_menu import marketplace_menu
            marketplace_menu()

        # 4. Logout
        elif choice == "4":
            console.print(
                "\n[bold red]Logging out... Returning to Login Menu.[/bold red]\n"
            )
            db.set_logged_in_user(None)
            from app.cli.login_menu import login_menu
            login_menu()
            break
