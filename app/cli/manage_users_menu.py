from rich.console import Console
from rich.prompt import Prompt
from app.services.user_service import view_users, add_user, delete_user

console = Console()

def manage_users_menu(current_user):
    while True:
        console.clear()
        console.print(f"[bold cyan]User Management[/bold cyan] (Logged in as: {current_user.username})")
        console.print("[1] View Users")
        console.print("[2] Add User")
        console.print("[3] Delete User")
        console.print("[4] Back\n")

        choice = Prompt.ask("[bold yellow]Enter your choice[/bold yellow]", choices=["1", "2", "3", "4"])

        if choice == "1":
            view_users()
            
        elif choice == "2":
            add_user(current_user)

        elif choice == "3":
            delete_user(current_user)

        elif choice == "4":
            break