from rich.console import Console
from rich.table import Table
from app.database.config import SessionLocal
from app.domain.portfolio import Portfolio
from app.domain.investment import Investment
from app.domain.transaction import TradeTransaction

console = Console()


def show_error(message: str) -> None:
    console.print(f"[bold red]Error:[/bold red] {message}")

def view_portfolios(current_user) -> None:
    """Show user portfolios and holdings from MySQL."""
    session = SessionLocal()
    try:
        portfolios = session.query(Portfolio).filter_by(user_id=current_user.id).all()

        if not portfolios:
            console.print("[yellow]You have no portfolios.[/yellow]")
            input("Press Enter to return...")
            return

        table = Table(title=f"{current_user.username}'s Portfolios")
        table.add_column("ID", justify="center")
        table.add_column("Name")
        table.add_column("Description")
        table.add_column("Balance", justify="right")

        for p in portfolios:
            table.add_row(str(p.id), p.name, p.description, f"${p.balance:,.2f}")

        console.print(table)

        
        for p in portfolios:
            investments = session.query(Investment).filter_by(portfolio_id=p.id).all()

            if investments:
                console.print(f"\n[bold cyan]Holdings in '{p.name}'[/bold cyan]")

                holdings_table = Table()
                holdings_table.add_column("Symbol")
                holdings_table.add_column("Qty")
                holdings_table.add_column("Purchase Price", justify="right")

                for inv in investments:
                    holdings_table.add_row(
                        inv.security_symbol,
                        str(inv.quantity),
                        f"${inv.purchase_price:,.2f}"
                    )

                console.print(holdings_table)
            else:
                console.print(f"\n[dim]No holdings in '{p.name}'[/dim]")

    except Exception as e:
        show_error(f"Could not display portfolios: {e}")

    finally:
        session.close()
        input("\nPress Enter to return...")

def view_transaction_history(portfolio):
    """Displays the transaction history for a portfolio."""
    session = SessionLocal()
    try:
        txs = session.query(TradeTransaction).filter(
            TradeTransaction.portfolio_id == portfolio.id
        ).order_by(TradeTransaction.timestamp.desc()).all()

        if not txs:
            console.print("[yellow]No transactions found for this portfolio.[/yellow]")
            return input("Press Enter to return...")

        table = Table(title="Transaction History")
        table.add_column("Date", justify="center")
        table.add_column("Type")
        table.add_column("Symbol")
        table.add_column("Qty", justify="right")
        table.add_column("Price", justify="right")
        table.add_column("Total", justify="right")

        for t in txs:
            total_val = t.quantity * t.price
            table.add_row(
                t.timestamp.strftime("%Y-%m-%d %H:%M"),
                t.transaction_type,
                t.security_symbol,
                str(t.quantity),
                f"${t.price:,.2f}",
                f"${total_val:,.2f}"
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error loading transactions: {e}[/red]")
    finally:
        session.close()
        input("Press Enter to return...")