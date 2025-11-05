from rich.console import Console
from rich.table import Table
import db
from app.domain.portfolio import Portfolio

console = Console()

def show_error(message: str) -> None:
    console.print(f"[bold red]Error:[/bold red] {message}")

def show_success(message: str) -> None:
    console.print(f"[bold green]{message}[/bold green]")

def create_portfolio() -> None:
    """Create a new portfolio with allocated balance."""
    try:
        user = db.logged_in_user
        name = input("Portfolio Name: ").strip()
        desc = input("Description: ").strip()

        while True:
            try:
                allocation = float(input(f"Amount to allocate from your balance (${user.balance:,.2f}): "))
                if allocation <= 0:
                    show_error("Amount must be greater than 0.")
                    continue
                if allocation > user.balance:
                    show_error("You cannot allocate more than your available balance.")
                    continue
                break
            except ValueError:
                show_error("Enter a valid numeric amount.")

        user.balance -= allocation
        pid = db.get_next_portfolio_id()
        new_p = Portfolio(pid, name, desc, allocation)
        db.portfolios.setdefault(user.username, []).append(new_p)
        show_success(f"Portfolio '{name}' created (ID {pid}) with ${allocation:,.2f} allocated.")
    except Exception as e:
        show_error(f"Could not create portfolio: {e}")

def delete_portfolio() -> None:
    """Delete portfolio if empty (no holdings)."""
    try:
        user = db.logged_in_user
        portfolios = db.portfolios.get(user.username, [])

        if not portfolios:
            console.print("[yellow]No portfolios available to delete.[/yellow]")
            input("Press Enter to continue...")
            return

        console.print("\n[bold cyan]Your Portfolios:[/bold cyan]")
        for p in portfolios:
            console.print(f"  ID: {p.id}  |  Name: {p.name}  |  Balance: ${p.balance:,.2f}")

        while True:
            try:
                pid = int(input("\nEnter Portfolio ID to delete: "))
            except ValueError:
                show_error("Please enter a valid numeric Portfolio ID.")
                continue

            portfolio = next((p for p in portfolios if p.id == pid), None)
            if not portfolio:
                show_error("Valid portfolio ID not found. Try again.")
                continue

            #Cannot delete portfolio with holdings
            if portfolio.holdings and len(portfolio.holdings) > 0:
                show_error("Cannot delete portfolio — it contains holdings. Please liquidate first.")
                return

            # Refund unused funds
            user.balance += portfolio.balance
            updated_list = [p for p in portfolios if p.id != pid]
            db.portfolios[user.username] = updated_list

            show_success(
                f"Portfolio '{portfolio.name}' deleted. "
                f"${portfolio.balance:,.2f} refunded to your balance."
            )
            break

    except Exception as e:
        show_error(f"Unexpected error: {e}")

def harvest_investment() -> None:
    """Sell (liquidate) an investment from a portfolio (partial or full)."""
    try:
        user = db.logged_in_user
        portfolios = db.portfolios.get(user.username, [])

        if not portfolios:
            console.print("[yellow]You have no portfolios.[/yellow]")
            input("Press Enter to continue...")
            return

        console.print("\n[bold cyan]Your Portfolios:[/bold cyan]")
        for p in portfolios:
            console.print(f"  ID: {p.id}  |  Name: {p.name}")

        # Portfolio ID
        while True:
            try:
                pid = int(input("\nEnter Portfolio ID: "))
            except ValueError:
                show_error("Please enter a valid numeric Portfolio ID.")
                continue

            portfolio = next((p for p in portfolios if p.id == pid), None)
            if not portfolio:
                show_error("Invalid portfolio ID. Try again.")
                continue
            break

        # Must have holdings
        if not portfolio.holdings:
            show_error("This portfolio has no holdings to liquidate.")
            return

        console.print("\n[bold cyan]Current Holdings:[/bold cyan]")
        for inv in portfolio.holdings:
            console.print(f"Ticker: {inv.ticker} | Quantity: {inv.quantity} | Purchase Price: ${inv.purchase_price:,.2f}")

        # Ticker selection
        ticker = input("\nEnter ticker to liquidate: ").upper().strip()
        investment = next((i for i in portfolio.holdings if i.ticker == ticker), None)
        if not investment:
            show_error("Investment not found in this portfolio.")
            return

        # Quantity
        while True:
            try:
                qty = int(input(f"Enter quantity to liquidate (max {investment.quantity}): "))
            except ValueError:
                show_error("Please enter a valid number.")
                continue
            if qty <= 0 or qty > investment.quantity:
                show_error("Invalid quantity. Must be between 1 and current holding.")
                continue
            break

        # Sale price
        while True:
            try:
                sale_price = float(input("Enter sale price per share: "))
                if sale_price <= 0:
                    show_error("Sale price must be greater than 0.")
                    continue
                break
            except ValueError:
                show_error("Please enter a valid numeric price.")

        # Calculate proceeds
        proceeds = qty * sale_price
        user.balance += proceeds
        portfolio.balance += proceeds  # add to portfolio cash

        # Update holdings
        if qty == investment.quantity:
            # Full liquidation
            portfolio.remove_investment(ticker)
            show_success(f"Fully liquidated {qty} shares of {ticker}. Proceeds: ${proceeds:,.2f}")
        else:
            # Partial liquidation
            investment.quantity -= qty
            show_success(f"Partially liquidated {qty} shares of {ticker}. Proceeds: ${proceeds:,.2f}")

        console.print(f"Updated Portfolio Balance: ${portfolio.balance:,.2f}")
        console.print(f"Updated User Balance: ${user.balance:,.2f}")

    except Exception as e:
        show_error(f"Unexpected error: {e}")
