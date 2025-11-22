from sqlalchemy import text
from core.database import engine

def reset_table():
    print("Connecting to database...")
    with engine.connect() as connection:
        print("Dropping old user_details table...")
        # We use COMMIT to ensure the changes happen immediately
        connection.execute(text("DROP TABLE IF EXISTS user_details CASCADE"))
        connection.commit()
        print("Table 'user_details' deleted successfully.")
        print("Please restart your server now to recreate it with new columns.")

if __name__ == "__main__":
    reset_table()