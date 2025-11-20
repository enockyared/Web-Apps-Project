from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from app.services import user_service

console = Console()

def manage_users_menu():
    """Admin-only Manage Users interface."""
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]Manage Users[/bold cyan]", border_style="cyan"))
        console.print("[1] View Users")
        console.print("[2] Add User")
        console.print("[3] Delete User")
        console.print("[4] Return to Main Menu\n")

        choice = Prompt.ask("[bold yellow]Enter your choice[/bold yellow]", choices=["1", "2", "3", "4"])

        if choice == "1":
            user_service.view_users()
            input("\nPress Enter to continue...")

        elif choice == "2":
            user_service.add_user()
            input("\nPress Enter to continue...")

        elif choice == "3":
            user_service.delete_user()
            input("\nPress Enter to continue...")

        elif choice == "4":
            break
