from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from app.services.user_service import get_user

console = Console()

def show_error(message: str) -> None:
    console.print(f"[bold red]Error:[/bold red] {message}")

def show_success(message: str) -> None:
    console.print(f"[bold green]{message}[/bold green]")

def login_menu():
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

            user = get_user(username)

            if user and user.password == password:
                show_success(f"\nLogin successful. Welcome {user.first_name}!\n")
                
                from app.cli.main_menu import main_menu
                return main_menu(user)  

            else:
                show_error("Invalid username or password. Please try again.")