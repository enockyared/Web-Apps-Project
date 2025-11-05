from rich.table import Table
from rich.console import Console
import db
from app.domain.user import User

console = Console()

def show_error(message: str) -> None:
    console.print(f"[bold red]Error:[/bold red] {message}")

def show_success(message: str) -> None:
    console.print(f"[bold green]{message}[/bold green]")

def view_users() -> None:
    """Display all registered users."""
    try:
        table = Table(title="Registered Users")
        table.add_column("Username")
        table.add_column("First Name")
        table.add_column("Last Name")
        table.add_column("Balance", justify="right")

        for u in db.users.values():
            table.add_row(u.username, u.first_name, u.last_name, f"${u.balance:,.2f}")

        console.print(table)
    except Exception as e:
        show_error(f"Could not load users: {e}")
    input("\nPress Enter to return...")

def add_user() -> None:
    """Add a new user."""
    console.print("[bold cyan]Add New User[/bold cyan]\n")
    try:
        first = input("First Name: ").strip()
        last  = input("Last Name: ").strip()
        username = input("Username: ").strip()
        if username in db.users:
            show_error("Username already exists.")
            return
        password = input("Password: ").strip()
        balance  = float(input("Initial Balance: "))
        new_user = User(first, last, username, password, balance)
        db.add_user(new_user)
        show_success(f"User '{username}' created successfully.")
    except ValueError:
        show_error("Balance must be a number.")
    except Exception as e:
        show_error(f"Unexpected error: {e}")

def delete_user() -> None:
    """Delete a user."""
    try:
        username = input("Enter username to delete: ").strip()
        if username not in db.users:
            show_error("User not found.")
            return
        if username == "eyared":
            show_error("Cannot delete the admin user.")
            return
        if username in db.portfolios and db.portfolios[username]:
            show_error("User has existing portfolios. Remove them first.")
            return
        del db.users[username]
        show_success(f"User '{username}' deleted.")
    except Exception as e:
        show_error(f"Unexpected error: {e}")
