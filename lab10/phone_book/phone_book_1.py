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
    """Create the phone_book table if it doesn't exist."""
    sql = (
        """
        CREATE TABLE IF NOT EXISTS phone_book (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(150) NOT NULL,
            phone_num VARCHAR(15) NOT NULL
        )
        """
    )
    with conn.cursor() as cur:
        cur.execute(sql)
    print("[OK] Table `phone_book` is ready.")


def insert_from_csv(conn):
    """Bulk-load data from a CSV file into the table."""
    path = input("Enter path to CSV file: ")
    sql = "COPY phone_book(user_name, phone_num) FROM %s DELIMITER ',' CSV HEADER"
    with conn.cursor() as cur:
        cur.execute(sql, (path,))
    print(f"[OK] Imported data from {path}.")


def insert_multiple_console(conn):
    """Insert multiple users from console input."""
    n = int(input("How many users to add? "))
    print("Enter USER NAME and PHONE NUMBER separated by space:")
    with conn.cursor() as cur:
        for _ in range(n):
            name, phone = input().split()
            cur.execute(
                "INSERT INTO phone_book(user_name, phone_num) VALUES (%s, %s)",
                (name, phone)
            )
    print("[OK] Batch insert complete.")


def update_phone_by_name(conn):
    """Update phone number for a given user name."""
    name = input("Enter user name: ")
    new_phone = input("Enter new phone number: ")
    sql = "UPDATE phone_book SET phone_num = %s WHERE user_name = %s"
    with conn.cursor() as cur:
        cur.execute(sql, (new_phone, name))
    print(f"[OK] Phone for '{name}' updated.")


def update_name_by_phone(conn):
    """Update user name for a given phone number."""
    phone = input("Enter current phone number: ")
    new_name = input("Enter new user name: ")
    sql = "UPDATE phone_book SET user_name = %s WHERE phone_num = %s"
    with conn.cursor() as cur:
        cur.execute(sql, (new_name, phone))
    print(f"[OK] Name for phone '{phone}' updated.")


def update_row_by_id(conn):
    """Update both name and phone for a specific user ID."""
    uid = int(input("Enter user ID: "))
    new_name = input("Enter new name: ")
    new_phone = input("Enter new phone number: ")
    sql = "UPDATE phone_book SET user_name = %s, phone_num = %s WHERE user_id = %s"
    with conn.cursor() as cur:
        cur.execute(sql, (new_name, new_phone, uid))
    print(f"[OK] Row {uid} updated.")


def query_phone_contains(conn):
    """Fetch users whose phone numbers contain a substring."""
    substr = input("Enter substring to search in phone numbers: ")
    sql = "SELECT user_id, user_name, phone_num FROM phone_book WHERE phone_num LIKE %s"
    with conn.cursor() as cur:
        cur.execute(sql, (f"%{substr}%",))
        rows = cur.fetchall()
    for r in rows:
        print(r)
    print(f"[OK] {len(rows)} record(s) found.")


def query_id_leq(conn):
    """Fetch users whose IDs are less than or equal to a value."""
    limit = int(input("Enter max user ID: "))
    sql = "SELECT user_name, phone_num FROM phone_book WHERE user_id <= %s"
    with conn.cursor() as cur:
        cur.execute(sql, (limit,))
        rows = cur.fetchall()
    for r in rows:
        print(r)
    print(f"[OK] {len(rows)} record(s) found.")


def delete_by_name(conn):
    """Delete entries matching a user name."""
    name = input("Enter user name to delete: ")
    sql = "DELETE FROM phone_book WHERE user_name = %s"
    with conn.cursor() as cur:
        cur.execute(sql, (name,))
    print(f"[OK] Deleted records with name '{name}'.")


def main():
    conn = None
    try:
        conn = connect_db()
        create_table(conn)
        menu = {
            '1': (insert_from_csv, 'Import from CSV'),
            '2': (insert_multiple_console, 'Batch insert from console'),
            '3': (update_phone_by_name, 'Update phone by name'),
            '4': (update_name_by_phone, 'Update name by phone'),
            '5': (update_row_by_id, 'Update both fields by ID'),
            '6': (query_phone_contains, "Query phone numbers containing"),
            '7': (query_id_leq, 'Query IDs <= value'),
            '8': (delete_by_name, 'Delete by name'),
            '0': (None, 'Exit')
        }

        while True:
            print("\n--- PHONE BOOK MENU ---")
            for key, (_, desc) in menu.items():
                print(f"{key}. {desc}")
            choice = input("Select an option: ")
            if choice == '0':
                break
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
