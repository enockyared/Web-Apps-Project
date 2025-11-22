from rich.console import Console
from rich.prompt import Prompt
from app.services import marketplace_service

console = Console()

def marketplace_menu(current_user):
    """Menu for viewing and buying securities."""
    while True:
        console.clear()
        console.print("[bold cyan]Marketplace[/bold cyan]")
        console.print("[1] View Securities")
        console.print("[2] Place Buy Order")
        console.print("[3] Return to Main Menu\n")

        choice = Prompt.ask("Select an option", choices=["1", "2", "3"])

        if choice == "1":
            marketplace_service.view_securities()
        elif choice == "2":
            marketplace_service.place_buy_order(current_user)
        elif choice == "3":
            break