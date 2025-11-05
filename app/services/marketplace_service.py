from rich.table import Table
from rich.console import Console
import db
from app.domain.investment import Investment
from app.services.portfolio_view_service import view_portfolios  # 👈 added import

console = Console()

def show_error(message: str) -> None:
    console.print(f"[bold red]Error:[/bold red] {message}")

def show_success(message: str) -> None:
    console.print(f"[bold green]{message}[/bold green]")

def view_securities() -> None:
    """Display available securities with remaining quantity."""
    try:
        table = Table(title="Available Securities to Buy")
        table.add_column("Ticker")
        table.add_column("Issuer")
        table.add_column("Price", justify="right")
        table.add_column("Available Qty", justify="right")

        for sec in db.securities.values():
            table.add_row(sec.ticker, sec.issuer, f"${sec.price:,.2f}", str(sec.available_quantity))

        console.print(table)
    except Exception as e:
        show_error(f"Could not load securities: {e}")
    input("Press Enter to return...")

def place_buy_order() -> None:
    """Buy a security respecting portfolio balance and stock availability."""
    try:
        user = db.logged_in_user

        # Portfolios accessible to user
        if user.username == "eyared":  # admin sees all portfolios
            accessible = [(uname, p) for uname, plist in db.portfolios.items() for p in plist]
        else:
            accessible = [(user.username, p) for p in db.portfolios.get(user.username, [])]

        if not accessible:
            console.print("[yellow]No portfolios available for purchase.[/yellow]")
            input("Press Enter to return...")
            return

        console.print("\n[bold cyan]Available Portfolios to Buy Into:[/bold cyan]")
        for owner, p in accessible:
            owner_tag = f" (owner: {owner})" if user.username == "eyared" else ""
            console.print(f"  ID: {p.id}  |  Name: {p.name}{owner_tag}  |  Balance: ${p.balance:,.2f}")

        # Portfolio selection
        while True:
            try:
                pid = int(input("\nEnter Portfolio ID: "))
            except ValueError:
                show_error("Please enter a numeric Portfolio ID.")
                continue
            portfolio = next((p for _, p in accessible if p.id == pid), None)
            if not portfolio:
                show_error("Valid portfolio ID not found. Try again.")
                continue
            break

        # Show all securities before asking for ticker
        console.print("\n[bold magenta]Available Securities to Buy:[/bold magenta]")
        sec_table = Table(title="Market Securities")
        sec_table.add_column("Ticker")
        sec_table.add_column("Issuer")
        sec_table.add_column("Price", justify="right")
        sec_table.add_column("Available Qty", justify="right")
        for sec in db.securities.values():
            sec_table.add_row(sec.ticker, sec.issuer, f"${sec.price:,.2f}", str(sec.available_quantity))
        console.print(sec_table)

        # Ticker selection
        while True:
            ticker = input("\nEnter the ticker symbol of the security to buy: ").upper().strip()
            sec = db.securities.get(ticker)
            if not sec:
                show_error("Invalid ticker symbol. Try again.")
            else:
                break

        # Quantity selection
        while True:
            try:
                qty = int(input(f"Enter quantity of {ticker} to buy: "))
                if qty <= 0:
                    show_error("Quantity must be greater than 0.")
                    continue
                break
            except ValueError:
                show_error("Quantity must be a number.")

        # Validate cost and quantity
        cost = sec.price * qty
        if qty > sec.available_quantity:
            show_error(f"Only {sec.available_quantity} shares available for {ticker}.")
            return
        if cost > portfolio.balance:
            show_error(f"Insufficient portfolio balance (${portfolio.balance:,.2f}).")
            return

        # Execute transaction
        portfolio.balance -= cost
        sec.available_quantity -= qty

        existing = next((i for i in portfolio.holdings if i.ticker == ticker), None)
        if existing:
            existing.quantity += qty
        else:
            portfolio.add_investment(Investment(ticker, qty, sec.price))

 
        console.print("\n[bold green]Buy Order Completed Successfully![/bold green]")
        show_success(
            f"Bought {qty} shares of {ticker} for ${cost:,.2f}.\n"
            f"Remaining portfolio balance: ${portfolio.balance:,.2f}\n"
            f"Remaining market supply for {ticker}: {sec.available_quantity} shares."
        )

        #Automatically show updated portfolios
        console.print("\n[bold cyan]Updated Portfolio Overview:[/bold cyan]")
        view_portfolios()

    except Exception as e:
        show_error(f"Unexpected error: {e}")
