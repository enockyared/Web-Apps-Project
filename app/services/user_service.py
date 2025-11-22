from rich.table import Table
from rich.console import Console
from app.domain.user import User
from app.database.config import SessionLocal
import re

console = Console()


def show_error(message: str) -> None:
    console.print(f"[bold red]Error:[/bold red] {message}")


def show_success(message: str) -> None:
    console.print(f"[bold green]{message}[/bold green]")

def get_user(username: str):
    session = SessionLocal()
    user = session.query(User).filter(User.username == username).first()
    session.close()
    return user

def view_users() -> None:
    """Display all registered users from DB."""
    try:
        session = SessionLocal()
        users = session.query(User).all()

        table = Table(title="Registered Users")
        table.add_column("Username")
        table.add_column("First Name")
        table.add_column("Last Name")
        table.add_column("Balance", justify="right")

        for u in users:
            table.add_row(u.username, u.first_name, u.last_name, f"${u.balance:,.2f}")

        console.print(table)

    except Exception as e:
        show_error(f"Could not load users: {e}")
    input("\nPress Enter to return...")


def add_user(current_user):
    session = SessionLocal()
    try:
        console.print("\n[bold cyan]Create New User[/bold cyan]")

        # ✨ Validate first and last name (letters only)
        while True:
            first_name = input("Enter first name: ").strip()
            if re.match(r"^[A-Za-z]+$", first_name):
                break
            console.print("[red]First name must contain only letters.[/red]")

        while True:
            last_name = input("Enter last name: ").strip()
            if re.match(r"^[A-Za-z]+$", last_name):
                break
            console.print("[red]Last name must contain only letters.[/red]")

        # ✨ Username with alphanumeric only
        while True:
            username = input("Enter username: ").strip()
            if not re.match(r"^[A-Za-z0-9]+$", username):
                console.print("[red]Username can only contain letters and numbers.[/red]")
                continue

            # Check availability
            existing_user = session.query(User).filter_by(username=username).first()
            if existing_user:
                console.print(f"[bold red]Error:[/bold red] Username '{username}' is already taken.")
            else:
                break

        password = input("Enter password: ").strip()
        balance = float(input("Enter starting balance: $").strip())

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            balance=balance
        )

        session.add(new_user)
        session.commit()
        console.print(f"[green]User '{username}' successfully created.[/green]")

    except Exception as e:
        session.rollback()
        console.print(f"[bold red]Unexpected error: {e}[/bold red]")

    finally:
        session.close()
        input("\nPress Enter to return...")


def delete_user(current_user):
    session = SessionLocal()
    try:
        console.print("\n[bold cyan]Delete User[/bold cyan]")

        users = session.query(User).all()

        if not users:
            console.print("[yellow]No users in system.[/yellow]")
            input("Press Enter to return...")
            return

        table = Table(title="Existing Users")
        table.add_column("Username")
        table.add_column("Balance", justify="right")

        for u in users:
            table.add_row(u.username, f"${u.balance:,.2f}")

        console.print(table)

        username = input("\nEnter username to delete: ").strip()
        user = session.query(User).filter_by(username=username).first()

        if not user:
            console.print("[red]User not found.[/red]")
            input("Press Enter to return...")
            return

        if user.id == current_user.id:
            console.print("[red]You cannot delete your own account while logged in.[/red]")
            input("Press Enter to return...")
            return

        session.delete(user)
        session.commit()

        show_success(f"User '{username}' deleted successfully.")

    except Exception as e:
        session.rollback()
        show_error(f"Unexpected error: {e}")

    finally:
        session.close()
        input("Press Enter to return...")