from rich.console import Console
from rich.table import Table
from app.database.config import SessionLocal
from app.domain.portfolio import Portfolio
from app.domain.investment import Investment
from app.domain.security import Security
from app.domain.transaction import TradeTransaction

console = Console()

def show_error(message: str) -> None:
    console.print(f"[bold red]Error:[/bold red] {message}")

def show_success(message: str) -> None:
    console.print(f"[bold green]{message}[/bold green]")

def create_portfolio(current_user) -> None:
    """Create a new portfolio stored in MySQL."""
    session = SessionLocal()
    try:
        console.print("\n[bold cyan]Create New Portfolio[/bold cyan]\n")

        name = input("Portfolio Name: ").strip()
        desc = input("Description: ").strip()

        while True:
            try:
                allocation = float(input(f"Amount to allocate (Your balance: ${current_user.balance:,.2f}): "))
                if allocation <= 0:
                    show_error("Amount must be greater than 0.")
                    continue
                if allocation > current_user.balance:
                    show_error("Amount exceeds available balance.")
                    continue
                break
            except ValueError:
                show_error("Enter a valid numeric amount.")

        db_user = session.merge(current_user)
        db_user.balance -= allocation

        new_portfolio = Portfolio(
            name=name,
            description=desc,
            balance=allocation,
            user_id=db_user.id
        )

        session.add(new_portfolio)
        session.commit()

        show_success(f"Portfolio '{name}' created successfully with ${allocation:,.2f} allocated.")

    except Exception as e:
        session.rollback()
        show_error(f"Could not create portfolio: {e}")

    finally:
        session.close()

    input("\nPress Enter to return...")

def delete_portfolio(current_user):
    session = SessionLocal()
    try:
        portfolios = session.query(Portfolio).filter_by(user_id=current_user.id).all()
        if not portfolios:
            console.print("[yellow]No portfolios available to delete.[/yellow]")
            input("Press Enter to continue...")
            return

        console.print("\n[bold cyan]Your Portfolios:[/bold cyan]")
        for p in portfolios:
            console.print(f"  ID: {p.id} | {p.name} | Balance: ${p.balance:,.2f}")

        pid = int(input("\nEnter Portfolio ID to delete: "))
        portfolio = session.query(Portfolio).filter_by(id=pid, user_id=current_user.id).first()

        if not portfolio:
            show_error("Portfolio not found.")
            return

        
        holdings = session.query(Investment).filter_by(portfolio_id=portfolio.id).all()
        if holdings:
            show_error("Cannot delete portfolio — holdings exist. Please liquidate first.")
            return

        
        current_user.balance += portfolio.balance
        session.delete(portfolio)
        session.commit()

        show_success(f"Portfolio '{portfolio.name}' deleted and ${portfolio.balance:,.2f} refunded.")

    except Exception as e:
        session.rollback()
        show_error(f"Unexpected error: {e}")

    finally:
        session.close()
        input("Press Enter to return to menu...")

def harvest_investment(current_user):
    session = SessionLocal()
    try:
        console.print("\n[bold cyan]Harvest Investment (Sell)[/bold cyan]")

        portfolios = session.query(Portfolio).filter_by(user_id=current_user.id).all()
        console.print("\nYour Portfolios:")
        for p in portfolios:
            console.print(f"  ID: {p.id} | {p.name} | Balance: ${p.balance:,.2f}")

        pid = int(input("\nEnter Portfolio ID to sell from: "))
        portfolio = session.query(Portfolio).filter_by(id=pid, user_id=current_user.id).first()
        if not portfolio:
            show_error("Invalid portfolio ID")
            return input("Press Enter to return...")

        investments = session.query(Investment).filter_by(portfolio_id=portfolio.id).all()

        console.print(f"\n[bold cyan]Holdings in '{portfolio.name}'[/bold cyan]")
        table = Table(title="Portfolio Holdings")
        table.add_column("Symbol")
        table.add_column("Qty")
        table.add_column("Purchase Price", justify="right")

        for inv in investments:
            table.add_row(inv.security_symbol, str(inv.quantity), f"${inv.purchase_price:,.2f}")

        console.print(table)

        symbol = input("\nEnter ticker to sell: ").strip().upper()
        investment = session.query(Investment).filter_by(
            portfolio_id=portfolio.id,
            security_symbol=symbol
        ).first()

        if not investment:
            show_error("No holdings found for this ticker.")
            return input("Press Enter to return...")

        qty = float(input(f"Enter quantity to sell (max {investment.quantity}): "))

        if qty > investment.quantity:
            show_error("Cannot sell more than owned.")
            return input("Press Enter to return...")

        sale_price = float(input("Enter sale price per share: "))

        investment.quantity -= qty
        portfolio.balance += qty * sale_price

        if investment.quantity == 0:
            session.delete(investment)

        sec = session.query(Security).filter(Security.symbol == symbol).first()
        sec.available_qty += qty

        # Log transaction
        tx = TradeTransaction(
            user_id=current_user.id,
            portfolio_id=portfolio.id,
            security_symbol=symbol,
            quantity=qty,
            price=sale_price,
            transaction_type="SELL"
        )

        session.add(tx)
        session.commit()

        show_success(f"Sold {qty} shares of {symbol} at ${sale_price:,.2f}")

    except Exception as e:
        session.rollback()
        show_error(f"Unexpected error: {e}")

    finally:
        session.close()
        input("Press Enter to return...")