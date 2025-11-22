from app.cli.login_menu import login_menu
from app.database.config import Base, engine, SessionLocal
from app.domain.user import User
from app.domain.portfolio import Portfolio
from app.domain.investment import Investment
from app.domain.security import Security
from app.domain.transaction import TradeTransaction
# Create all database tables
Base.metadata.create_all(bind=engine)

# Seed admin user if not exists
def seed_admin():
    session = SessionLocal()
    existing_admin = session.query(User).filter(User.username == "eyared").first()
    if not existing_admin:
        admin = User("Enock", "Yared", "eyared", "admin123", 25000.00)
        session.add(admin)
        session.commit()
        print("[Admin] Default admin user created.")
    session.close()

if __name__ == "__main__":
    seed_admin()
    login_menu()