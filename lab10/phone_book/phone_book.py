import psycopg2
from config import host, user, password, db_name


def connect_db():
    """Establish and return a PostgreSQL connection."""
    try:
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        conn.autocommit = True
        return conn
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        exit(1)


def create_table(conn):
    """Create the phone_book table if it doesn't exist."""
    sql = """
        CREATE TABLE IF NOT EXISTS phone_book (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(150) NOT NULL,
            phone_num VARCHAR(15) NOT NULL
        )
    """
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        print("[OK] Table `phone_book` is ready.")
    except Exception as e:
        print(f"[ERROR] Failed to create table: {e}")


# --- INSERT OPERATIONS ---

def insert_from_csv(conn):
    """Bulk-load data from a CSV file into the table."""
    path = input("Enter path to CSV file: ")
    try:
        with open(path, 'r') as f:
            # Skip header
            next(f)
            
            with conn.cursor() as cur:
                cur.copy_expert(
                    "COPY phone_book(user_name, phone_num) FROM STDIN WITH CSV",
                    f
                )
        print(f"[OK] Imported data from {path}.")
    except FileNotFoundError:
        print(f"[ERROR] File {path} not found. Please check the file path.")
    except Exception as e:
        print(f"[ERROR] CSV import failed: {e}")


def insert_from_console(conn):
    """Insert a single user from console input."""
    try:
        name = input("Enter user name: ")
        phone = input("Enter phone number: ")
        
        # Basic validation
        if not name or not phone:
            print("[ERROR] Name and phone cannot be empty.")
            return
            
        sql = "INSERT INTO phone_book(user_name, phone_num) VALUES (%s, %s)"
        with conn.cursor() as cur:
            cur.execute(sql, (name, phone))
        print(f"[OK] Added {name} -> {phone}.")
    except Exception as e:
        print(f"[ERROR] Insert failed: {e}")


# --- UPDATE OPERATIONS ---

def update_name_by_phone(conn):
    """Update user name for a given phone number."""
    try:
        phone = input("Enter phone number to find user: ")
        new_name = input("Enter new user name: ")
        
        # Check if the phone exists
        check_sql = "SELECT COUNT(*) FROM phone_book WHERE phone_num = %s"
        with conn.cursor() as cur:
            cur.execute(check_sql, (phone,))
            if cur.fetchone()[0] == 0:
                print(f"[ERROR] No user found with phone number {phone}.")
                return
                
        sql = "UPDATE phone_book SET user_name = %s WHERE phone_num = %s"
        with conn.cursor() as cur:
            cur.execute(sql, (new_name, phone))
            rows_updated = cur.rowcount
        print(f"[OK] Updated {rows_updated} record(s). Name for phone '{phone}' is now '{new_name}'.")
    except Exception as e:
        print(f"[ERROR] Update failed: {e}")


def update_phone_by_name(conn):
    """Update phone number for a given user name."""
    try:
        name = input("Enter user name to find: ")
        new_phone = input("Enter new phone number: ")
        
        # Check if the name exists
        check_sql = "SELECT COUNT(*) FROM phone_book WHERE user_name = %s"
        with conn.cursor() as cur:
            cur.execute(check_sql, (name,))
            if cur.fetchone()[0] == 0:
                print(f"[ERROR] No user found with name {name}.")
                return
                
        sql = "UPDATE phone_book SET phone_num = %s WHERE user_name = %s"
        with conn.cursor() as cur:
            cur.execute(sql, (new_phone, name))
            rows_updated = cur.rowcount
        print(f"[OK] Updated {rows_updated} record(s). Phone for '{name}' is now '{new_phone}'.")
    except Exception as e:
        print(f"[ERROR] Update failed: {e}")


# --- QUERY OPERATIONS ---

def query_by_name_pattern(conn):
    """Query users by name pattern."""
    try:
        pattern = input("Enter name pattern (use % as wildcard): ")
        sql = "SELECT user_id, user_name, phone_num FROM phone_book WHERE user_name LIKE %s ORDER BY user_id"
        
        with conn.cursor() as cur:
            cur.execute(sql, (pattern,))
            rows = cur.fetchall()
            
        if rows:
            print("\nResults:")
            print("ID\tName\t\tPhone")
            print("-" * 40)
            for uid, name, phone in rows:
                print(f"{uid}\t{name}\t\t{phone}")
            print(f"\n[OK] {len(rows)} record(s) found.")
        else:
            print("[INFO] No matching records found.")
    except Exception as e:
        print(f"[ERROR] Query failed: {e}")


def query_by_phone_pattern(conn):
    """Query users by phone number pattern."""
    try:
        pattern = input("Enter phone pattern (use % as wildcard): ")
        sql = "SELECT user_id, user_name, phone_num FROM phone_book WHERE phone_num LIKE %s ORDER BY user_id"
        
        with conn.cursor() as cur:
            cur.execute(sql, (pattern,))
            rows = cur.fetchall()
            
        if rows:
            print("\nResults:")
            print("ID\tName\t\tPhone")
            print("-" * 40)
            for uid, name, phone in rows:
                print(f"{uid}\t{name}\t\t{phone}")
            print(f"\n[OK] {len(rows)} record(s) found.")
        else:
            print("[INFO] No matching records found.")
    except Exception as e:
        print(f"[ERROR] Query failed: {e}")


def query_all_records(conn):
    """Display all records in the phone book."""
    try:
        sql = "SELECT user_id, user_name, phone_num FROM phone_book ORDER BY user_id"
        
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            
        if rows:
            print("\nAll Phone Book Records:")
            print("ID\tName\t\tPhone")
            print("-" * 40)
            for uid, name, phone in rows:
                print(f"{uid}\t{name}\t\t{phone}")
            print(f"\n[OK] Total {len(rows)} record(s).")
        else:
            print("[INFO] Phone book is empty.")
    except Exception as e:
        print(f"[ERROR] Query failed: {e}")


# --- DELETE OPERATIONS ---

def delete_by_name(conn):
    """Delete entries by user name."""
    try:
        name = input("Enter user name to delete: ")
        
        # Check if the name exists
        check_sql = "SELECT COUNT(*) FROM phone_book WHERE user_name = %s"
        with conn.cursor() as cur:
            cur.execute(check_sql, (name,))
            if cur.fetchone()[0] == 0:
                print(f"[ERROR] No user found with name {name}.")
                return
                
        sql = "DELETE FROM phone_book WHERE user_name = %s"
        with conn.cursor() as cur:
            cur.execute(sql, (name,))
            rows_deleted = cur.rowcount
        print(f"[OK] Deleted {rows_deleted} record(s) with name '{name}'.")
    except Exception as e:
        print(f"[ERROR] Delete failed: {e}")


def delete_by_phone(conn):
    """Delete entries by phone number."""
    try:
        phone = input("Enter phone number to delete: ")
        
        # Check if the phone exists
        check_sql = "SELECT COUNT(*) FROM phone_book WHERE phone_num = %s"
        with conn.cursor() as cur:
            cur.execute(check_sql, (phone,))
            if cur.fetchone()[0] == 0:
                print(f"[ERROR] No user found with phone number {phone}.")
                return
                
        sql = "DELETE FROM phone_book WHERE phone_num = %s"
        with conn.cursor() as cur:
            cur.execute(sql, (phone,))
            rows_deleted = cur.rowcount
        print(f"[OK] Deleted {rows_deleted} record(s) with phone number '{phone}'.")
    except Exception as e:
        print(f"[ERROR] Delete failed: {e}")


def main():
    conn = None
    try:
        # Connect to database and setup table
        conn = connect_db()
        create_table(conn)
        
        menu = {
            # Insert operations
            '1': (insert_from_csv, 'Import from CSV file'),
            '2': (insert_from_console, 'Add single user from console'),
            
            # Update operations
            '3': (update_name_by_phone, 'Update name by phone number'),
            '4': (update_phone_by_name, 'Update phone by user name'),
            
            # Query operations
            '5': (query_by_name_pattern, 'Search by name pattern'),
            '6': (query_by_phone_pattern, 'Search by phone pattern'),
            '7': (query_all_records, 'View all records'),
            
            # Delete operations
            '8': (delete_by_name, 'Delete by user name'),
            '9': (delete_by_phone, 'Delete by phone number'),
            
            '0': (None, 'Exit')
        }

        while True:
            print("\n" + "=" * 40)
            print("        PHONE BOOK MANAGEMENT")
            print("=" * 40)
            
            # Display menu groups
            print("\nINSERT OPERATIONS:")
            print("1. Import from CSV file")
            print("2. Add single user from console")
            
            print("\nUPDATE OPERATIONS:")
            print("3. Update name by phone number")
            print("4. Update phone by user name")
            
            print("\nQUERY OPERATIONS:")
            print("5. Search by name pattern")
            print("6. Search by phone pattern")
            print("7. View all records")
            
            print("\nDELETE OPERATIONS:")
            print("8. Delete by user name")
            print("9. Delete by phone number")
            
            print("\n0. Exit")
            
            choice = input("\nSelect an option: ")
            
            if choice == '0':
                print("[INFO] Exiting program.")
                break
                
            action = menu.get(choice)
            if action:
                action[0](conn)
            else:
                print("[ERROR] Invalid option.")

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        if conn:
            conn.close()
            print("[INFO] Database connection closed.")


if __name__ == '__main__':
    main()