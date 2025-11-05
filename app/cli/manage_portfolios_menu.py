from rich.console import Console
from app.services.portfolio_view_service import view_portfolios
from app.services.portfolio_manage_service import create_portfolio, delete_portfolio, harvest_investment
import db

console = Console()

def manage_portfolios_menu() -> None:
    """Manage Portfolios menu for logged-in users (admin & regular)."""
    while True:
        console.print("\n[bold blue]--- Manage Portfolios Menu ---[/bold blue]")

        user = db.logged_in_user

        console.print("1. View Portfolios")
        console.print("2. Create New Portfolio")
        console.print("3. Delete Portfolio")
        console.print("4. Harvest Investment (Sell)")
        console.print("5. Return to Main Menu")

        try:
            choice = int(input("\nEnter your choice: ").strip())

            if choice == 1:
                # Admin sees all, regular user sees their own
                view_portfolios()
            elif choice == 2:
                create_portfolio()
            elif choice == 3:
                delete_portfolio()
            elif choice == 4:
                harvest_investment()
            elif choice == 5:
                console.print("[yellow]Returning to Main Menu...[/yellow]")
                break
            else:
                console.print("[red]Invalid choice. Please select a number between 1 and 5.[/red]")

        except ValueError:
            console.print("[red]Invalid input. Please enter a number.[/red]")
        except Exception as e:
            console.print(f"[bold red]Unexpected error:[/bold red] {e}")
