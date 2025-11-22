from rich.console import Console
from rich.table import Table
from app.database.config import SessionLocal
from app.domain.security import Security
from app.domain.portfolio import Portfolio
from app.domain.investment import Investment
from app.domain.transaction import TradeTransaction

console = Console()

def show_error(message: str) -> None:
    console.print(f"[bold red]Error:[/bold red] {message}")

def show_success(message: str) -> None:
    console.print(f"[bold green]{message}[/bold green]")


def view_securities() -> None:
    """Display all available securities."""
    session = SessionLocal()
    try:
        securities = session.query(Security).all()

        if not securities:
            console.print("[yellow]No securities available in market.[/yellow]")
            input("Press Enter to return...")
            return

        table = Table(title="Available Securities")
        table.add_column("ID", justify="center")
        table.add_column("Symbol")
        table.add_column("Issuer")
        table.add_column("Price", justify="right")
        table.add_column("Available", justify="right")

        for sec in securities:
            table.add_row(
                str(sec.id), sec.symbol, sec.issuer,
                f"${sec.price:,.2f}", str(sec.available_qty)
            )
        
        console.print(table)

    except Exception as e:
        show_error(f"Error loading securities: {e}")

    finally:
        session.close()
        input("Press Enter to return...")


def place_buy_order(current_user):
    session = SessionLocal()
    try:
        portfolios = session.query(Portfolio).filter(Portfolio.user_id == current_user.id).all()
        if not portfolios:
            console.print("[yellow]No portfolios available for purchase.[/yellow]")
            return input("Press Enter to return...")

        console.print("\n[bold cyan]Your Portfolios:[/bold cyan]")
        for p in portfolios:
            console.print(f"  ID: {p.id} | {p.name} | Balance: ${p.balance:,.2f}")

        pid = int(input("\nEnter Portfolio ID to buy into: "))
        portfolio = session.query(Portfolio).filter(Portfolio.id == pid).first()
        if not portfolio:
            console.print("[red]Invalid portfolio ID[/red]")
            return input("Press Enter to return...")

        # List securities
        securities = session.query(Security).all()
        table = Table(title="Market Securities")
        table.add_column("ID")
        table.add_column("Symbol")
        table.add_column("Issuer")
        table.add_column("Price", justify="right")
        table.add_column("Available", justify="right")

        for s in securities:
            table.add_row(str(s.id), s.symbol, s.issuer, f"${s.price:,.2f}", str(s.available_qty))
        console.print(table)

        sid = int(input("\nEnter Security ID or Symbol to buy: "))
        sec = session.query(Security).filter(Security.id == sid).first()

        qty = float(input(f"Enter quantity of {sec.symbol}: "))
        total_cost = qty * sec.price

        if total_cost > portfolio.balance:
            console.print("[red]Insufficient balance[/red]")
            return input("Press Enter to return...")

        portfolio.balance -= total_cost
        sec.available_qty -= qty

        
        inv = Investment(
            security_symbol=sec.symbol,
            portfolio_id=portfolio.id,
            quantity=qty,
            purchase_price=sec.price
        )
        session.add(inv)

        
        tx = TradeTransaction(
            portfolio_id=portfolio.id,
            user_id=current_user.id,
            security_symbol=sec.symbol,
            quantity=qty,
            price=sec.price,
            transaction_type="BUY"
        )

        session.add(tx)

        session.commit()
        show_success(f"Buy completed: {qty} of {sec.symbol} @ {sec.price}")

    except Exception as e:
        session.rollback()
        show_error(f"Unexpected error: {e}")

    finally:
        session.close()
        input("Press Enter to return...")