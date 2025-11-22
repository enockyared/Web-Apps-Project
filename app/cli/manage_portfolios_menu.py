from rich.console import Console
from app.domain.portfolio import Portfolio 
from app.services.portfolio_view_service import view_portfolios
from app.services.portfolio_manage_service import create_portfolio, delete_portfolio, harvest_investment
from app.services.marketplace_service import show_error
console = Console()

def manage_portfolios_menu(current_user) -> None:
    """Manage Portfolios menu for logged-in users (admin & regular)."""
    while True:
        console.print("\n[bold blue]--- Manage Portfolios Menu ---[/bold blue]")

        console.print("1. View Portfolios")
        console.print("2. Create New Portfolio")
        console.print("3. Delete Portfolio")
        console.print("4. Harvest Investment (Sell)")
        console.print("5. View Transaction History")   
        console.print("6. Return to Main Menu")        

        try:
            choice = int(input("\nEnter your choice: ").strip())

            if choice == 1:
                view_portfolios(current_user)

            elif choice == 2:
                create_portfolio(current_user)

            elif choice == 3:
                delete_portfolio(current_user)

            elif choice == 4:
                harvest_investment(current_user)

            elif choice == 5:
                from app.database.config import SessionLocal   
                session = SessionLocal()                       

                port_list = session.query(Portfolio).filter_by(user_id=current_user.id).all()

                console.print("\n[bold cyan]Select Portfolio for Transaction History[/bold cyan]")
                for p in port_list:
                    console.print(f"  ID: {p.id} | {p.name} | Balance: ${p.balance:,.2f}")

                try:
                    pid = int(input("\nEnter Portfolio ID: "))
                    portfolio = session.query(Portfolio).filter_by(id=pid, user_id=current_user.id).first()

                    if not portfolio:
                        show_error("Invalid portfolio ID")
                    else:
                        from app.services.portfolio_view_service import view_transaction_history
                        view_transaction_history(portfolio)

                except ValueError:
                    show_error("Invalid input, please enter a number")

                finally:
                    session.close()

            elif choice == 6:
                console.print("[yellow]Returning to Main Menu...[/yellow]")
                break

            else:
                console.print("[red]Invalid choice. Select 1–6.[/red]")

        except ValueError:
            console.print("[red]Invalid input. Please enter a number.[/red]")
        except Exception as e:
            console.print(f"[bold red]Unexpected error:[/bold red] {e}")