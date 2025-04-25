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


def insert_from_csv(conn, path):
    """Bulk-load data from a CSV file into the table."""
    sql = (
        """
        COPY phone_book(user_name, phone_num)
        FROM %s DELIMITER ',' CSV HEADER
        """
    )
    with conn.cursor() as cur:
        cur.execute(sql, (path,))
    print(f"[OK] Imported data from {path}.")


def insert_user(conn):
    """Prompt for a single user and insert into the table."""
    name = input("Enter user name: ")
    phone = input("Enter phone number: ")
    sql = "INSERT INTO phone_book(user_name, phone_num) VALUES (%s, %s)"
    with conn.cursor() as cur:
        cur.execute(sql, (name, phone))
    print(f"[OK] Added {name} -> {phone}.")


def update_user(conn):
    """Update an existing user's name and/or phone by ID."""
    uid = input("Enter user ID to update: ")
    new_name = input("Enter new name (leave blank to skip): ")
    new_phone = input("Enter new phone (leave blank to skip): ")

    fields, params = [], []
    if new_name:
        fields.append("user_name = %s")
        params.append(new_name)
    if new_phone:
        fields.append("phone_num = %s")
        params.append(new_phone)
    if not fields:
        print("[WARN] Nothing to update.")
        return

    sql = f"UPDATE phone_book SET {', '.join(fields)} WHERE user_id = %s"
    params.append(uid)
    with conn.cursor() as cur:
        cur.execute(sql, params)
    print(f"[OK] User {uid} updated.")


def delete_user(conn):
    """Delete a user by name."""
    name = input("Enter user name to delete: ")
    sql = "DELETE FROM phone_book WHERE user_name = %s"
    with conn.cursor() as cur:
        cur.execute(sql, (name,))
    print(f"[OK] Deleted entries with name '{name}'.")


def query_users(conn):
    """Run a SELECT query based on user-specified condition."""
    cond = input("Enter SQL WHERE clause (e.g. phone_num LIKE '%54%'): ")
    sql = f"SELECT user_id, user_name, phone_num FROM phone_book WHERE {cond}"
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    if rows:
        print("Results:")
        for r in rows:
            print(r)
    else:
        print("[INFO] No matching records.")


def main():
    conn = None
    try:
        conn = connect_db()
        create_table(conn)

        options = {
            '1': (insert_from_csv, 'Import from CSV file'),
            '2': (insert_user, 'Add single user'),
            '3': (update_user, 'Update user by ID'),
            '4': (delete_user, 'Delete user by name'),
            '5': (query_users, 'Query phone book'),
            '0': (None, 'Exit')
        }

        while True:
            print("\n--- PHONE BOOK MENU ---")
            for k, (_, desc) in options.items():
                print(f"{k}. {desc}")
            choice = input("Select an option: ")
            if choice == '0':
                break
            action = options.get(choice)
            if action:
                func = action[0]
                if choice == '1':
                    path = input("Enter path to CSV file: ")
                    func(conn, path)
                else:
                    func(conn)
            else:
                print("[ERROR] Invalid option.")

    except Exception as ex:
        print("[ERROR]", ex)
    finally:
        if conn:
            conn.close()
            print("[INFO] Connection closed.")


if __name__ == '__main__':
    main()
