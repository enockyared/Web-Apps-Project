from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
import db

console = Console()

def login_menu():
    """Display the login menu and handle user authentication."""
    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]Welcome to the Investment App[/bold cyan]", border_style="cyan"))
        console.print("[1] Login")
        console.print("[2] Exit\n")

        choice = Prompt.ask("[bold yellow]Enter your choice[/bold yellow]", choices=["1", "2"])

        if choice == "2":
            console.print("\n[bold red]Exiting application... Goodbye![/bold red]")
            break

        elif choice == "1":
            username = Prompt.ask("[bold cyan]Enter username[/bold cyan]")
            password = Prompt.ask("[bold magenta]Enter password[/bold magenta]", password=True)

            user = db.get_user(username)
            if user and user.password == password:
                db.set_logged_in_user(user)
                console.print(f"\n[bold green]Login successful! Welcome, {user.first_name}.[/bold green]\n")
                from app.cli.main_menu import main_menu
                main_menu()
                break
            else:
                console.print("[bold red]Invalid username or password. Please try again.[/bold red]\n")
