import psycopg2
from config import host, user, password, db_name


def connect_db():
    """Establish and return a PostgreSQL connection."""
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    conn.autocommit = True
    return conn


def create_table(conn):
    """Create the phone_book table with name, surname, and phone if it doesn't exist."""
    sql = (
        """
        CREATE TABLE IF NOT EXISTS phone_book (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(150) NOT NULL,
            user_surname VARCHAR(150) NOT NULL,
            phone_num VARCHAR(15) NOT NULL
        )
        """
    )
    with conn.cursor() as cur:
        cur.execute(sql)
    print("[OK] Table `phone_book` is ready.")


def return_records(conn):
    """Fetch all records where name, surname, or phone contains a pattern via SQL function."""
    pattern = input("Enter search pattern: ")
    sql = "SELECT * FROM return_records(%s)"
    with conn.cursor() as cur:
        cur.execute(sql, (pattern,))
        rows = cur.fetchall()
    if rows:
        for r in rows:
            print(r)
    else:
        print("[INFO] No records found.")


def insert_or_update_user(conn):
    """Insert a new user or update phone if user exists via procedure or logic."""
    first, last, phone = input("Enter FIRST_NAME LAST_NAME PHONE: ").split()
    # Using Python logic rather than external proc
    check_sql = (
        "SELECT user_id FROM phone_book"
        " WHERE user_name = %s OR user_surname = %s"
    )
    with conn.cursor() as cur:
        cur.execute(check_sql, (first, last))
        existing = cur.fetchone()
        if existing:
            update_sql = (
                "UPDATE phone_book SET phone_num = %s"
                " WHERE user_id = %s"
            )
            cur.execute(update_sql, (phone, existing[0]))
            print(f"[OK] Updated phone for ID {existing[0]}.")
        else:
            insert_sql = (
                "INSERT INTO phone_book(user_name, user_surname, phone_num)"
                " VALUES (%s, %s, %s)"
            )
            cur.execute(insert_sql, (first, last, phone))
            print(f"[OK] Inserted {first} {last}.")


def get_data_paginated(conn):
    """Fetch paginated results filtered by phone substring via SQL function."""
    lim = int(input("Limit: "))
    off = int(input("Offset: "))
    pattern = input("Phone pattern (e.g. %123%): ")
    sql = "SELECT * FROM get_data(%s, %s, %s)"
    with conn.cursor() as cur:
        cur.execute(sql, (lim, off, pattern))
        rows = cur.fetchall()
    for r in rows:
        print(r)
    print(f"[OK] Retrieved {len(rows)} rows.")


def delete_by_name_or_surname(conn):
    """Delete records matching a name or surname."""
    name = input("Enter user name or surname to delete: ")
    sql = "DELETE FROM phone_book WHERE user_name = %s OR user_surname = %s"
    with conn.cursor() as cur:
        cur.execute(sql, (name, name))
    print(f"[OK] Deleted users matching '{name}'.")


def delete_by_phone(conn):
    """Delete records matching a phone number."""
    phone = input("Enter phone number to delete: ")
    sql = "DELETE FROM phone_book WHERE phone_num = %s"
    with conn.cursor() as cur:
        cur.execute(sql, (phone,))
    print(f"[OK] Deleted users with phone '{phone}'.")


def main():
    conn = None
    try:
        conn = connect_db()
        create_table(conn)
        menu = {
            '1': (return_records, 'Search records'),
            '2': (insert_or_update_user, 'Insert or update user'),
            '3': (get_data_paginated, 'Paginated query'),
            '4': (delete_by_name_or_surname, 'Delete by name/surname'),
            '5': (delete_by_phone, 'Delete by phone'),
            '0': (None, 'Exit')
        }
        while True:
            print("\n--- PHONE BOOK MENU ---")
            for k, (_, desc) in menu.items(): print(f"{k}. {desc}")
            choice = input("Select an option: ")
            if choice == '0': break
            action = menu.get(choice)
            if action:
                action[0](conn)
            else:
                print("[ERROR] Invalid option.")
    except Exception as e:
        print("[ERROR]", e)
    finally:
        if conn:
            conn.close()
            print("[INFO] Connection closed.")

if __name__ == '__main__':
    main()
