from rich.table import Table
from rich.console import Console
import db

console = Console()

def show_error(message: str) -> None:
    console.print(f"[bold red]Error:[/bold red] {message}")

def show_success(message: str) -> None:
    console.print(f"[bold green]{message}[/bold green]")

def view_portfolios() -> None:
    """Show portfolios and holdings.
       Admin sees all user portfolios."""
    try:
        user = db.logged_in_user

        # Admin sees all portfolios
        if user.username == "eyared":
            all_portfolios = []
            for uname, plist in db.portfolios.items():
                for p in plist:
                    all_portfolios.append((uname, p))

            if not all_portfolios:
                console.print("[yellow]No portfolios exist in the system.[/yellow]")
                input("Press Enter to continue...")
                return

            table = Table(title="All User Portfolios (Admin View)")
            table.add_column("Owner", justify="center")
            table.add_column("Portfolio ID", justify="center")
            table.add_column("Name")
            table.add_column("Description")
            table.add_column("Balance", justify="right")

            for owner, p in all_portfolios:
                table.add_row(owner, str(p.id), p.name, p.description, f"${p.balance:,.2f}")
            console.print(table)

            # Display holdings
            for owner, p in all_portfolios:
                if p.holdings:
                    console.print(f"\n[bold cyan]Holdings in '{p.name}' (Owner: {owner})[/bold cyan]")
                    holdings_table = Table()
                    holdings_table.add_column("Ticker")
                    holdings_table.add_column("Quantity")
                    holdings_table.add_column("Purchase Price", justify="right")
                    for inv in p.holdings:
                        holdings_table.add_row(inv.ticker, str(inv.quantity), f"${inv.purchase_price:,.2f}")
                    console.print(holdings_table)
                else:
                    console.print(f"\n[dim]No holdings in '{p.name}' (Owner: {owner})[/dim]")

        # Regular user
        else:
            portfolios = db.portfolios.get(user.username, [])
            if not portfolios:
                console.print("[yellow]You have no portfolios.[/yellow]")
                input("Press Enter to continue...")
                return

            table = Table(title=f"{user.username}'s Portfolios")
            table.add_column("ID", justify="center")
            table.add_column("Name")
            table.add_column("Description")
            table.add_column("Balance", justify="right")

            for p in portfolios:
                table.add_row(str(p.id), p.name, p.description, f"${p.balance:,.2f}")
            console.print(table)

            for p in portfolios:
                if p.holdings:
                    console.print(f"\n[bold cyan]Holdings in '{p.name}'[/bold cyan]")
                    holdings_table = Table()
                    holdings_table.add_column("Ticker")
                    holdings_table.add_column("Quantity")
                    holdings_table.add_column("Purchase Price", justify="right")
                    for inv in p.holdings:
                        holdings_table.add_row(inv.ticker, str(inv.quantity), f"${inv.purchase_price:,.2f}")
                    console.print(holdings_table)
                else:
                    console.print(f"\n[dim]No holdings in '{p.name}'[/dim]")

    except Exception as e:
        show_error(f"Could not display portfolios: {e}")
    input("\nPress Enter to continue...")

