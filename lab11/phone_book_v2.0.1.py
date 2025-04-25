import psycopg2
import psycopg2.extras
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


def setup_database(conn):
    """Create the phone_book table and setup all functions/procedures."""
    # First create the base table
    table_sql = """
        CREATE TABLE IF NOT EXISTS phone_book (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(150) NOT NULL,
            phone_num VARCHAR(15) NOT NULL
        )
    """
    
    try:
        with conn.cursor() as cur:
            cur.execute(table_sql)
        print("[OK] Table `phone_book` is ready.")
        
        # Now load all the functions and procedures from file
        with open('sql_functions.sql', 'r') as f:
            sql_functions = f.read()
            
        with conn.cursor() as cur:
            cur.execute(sql_functions)
        print("[OK] All database functions and procedures are installed.")
        
    except Exception as e:
        print(f"[ERROR] Database setup failed: {e}")
        exit(1)


# --- FUNCTION 1: SEARCH BY PATTERN ---

def search_by_pattern(conn):
    """Use the database function to search by pattern in name or phone."""
    try:
        pattern = input("Enter search pattern (part of name or phone): ")
        
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM find_contacts_by_pattern(%s)", (pattern,))
            rows = cur.fetchall()
            
        if rows:
            print("\nSearch Results:")
            print("ID\tName\t\tPhone")
            print("-" * 40)
            for uid, name, phone in rows:
                print(f"{uid}\t{name}\t\t{phone}")
            print(f"\n[OK] {len(rows)} record(s) found.")
        else:
            print("[INFO] No matching records found.")
    except Exception as e:
        print(f"[ERROR] Search failed: {e}")


# --- PROCEDURE 2: INSERT OR UPDATE USER ---

def upsert_user(conn):
    """Insert a new user or update phone if user exists."""
    try:
        name = input("Enter user name: ")
        phone = input("Enter phone number: ")
        
        # Basic validation
        if not name or not phone:
            print("[ERROR] Name and phone cannot be empty.")
            return
            
        with conn.cursor() as cur:
            cur.execute("CALL upsert_user(%s, %s)", (name, phone))
            
        print(f"[OK] User {name} processed successfully.")
    except Exception as e:
        print(f"[ERROR] Upsert operation failed: {e}")


# --- PROCEDURE 3: BULK INSERT WITH VALIDATION ---

def bulk_insert_users(conn):
    """Bulk insert users with validation in the database procedure."""
    try:
        num_users = int(input("How many users do you want to insert? "))
        if num_users <= 0:
            print("[ERROR] Number must be positive.")
            return
            
        names = []
        phones = []
        
        print("\nEnter user details (name and phone on separate lines):")
        for i in range(num_users):
            print(f"\nUser {i+1}:")
            name = input("Name: ")
            phone = input("Phone: ")
            names.append(name)
            phones.append(phone)
        
        # Call the stored procedure with arrays
        with conn.cursor() as cur:
            cur.execute(
                "CALL bulk_insert_users(%s, %s, NULL)", 
                (names, phones)
            )
            
            # Fetch notices that contain validation errors
            notices = conn.notices
            if notices:
                for notice in notices:
                    print(notice)
        
        print(f"[OK] Bulk insert of {num_users} users completed.")
        
    except ValueError:
        print("[ERROR] Please enter a valid number.")
    except Exception as e:
        print(f"[ERROR] Bulk insert failed: {e}")


# --- FUNCTION 4: PAGINATED QUERY ---

def paginated_query(conn):
    """Query the phone book with pagination."""
    try:
        print("\nPaginated Phone Book Query")
        page_size = int(input("Enter page size (records per page): "))
        if page_size <= 0:
            print("[ERROR] Page size must be positive.")
            return
            
        page_num = 1
        offset = 0
        sort_options = {
            '1': 'user_id',
            '2': 'user_name', 
            '3': 'phone_num'
        }
        
        print("\nSort by:")
        for key, value in sort_options.items():
            print(f"{key}. {value}")
        sort_choice = input("Select option (default: user_id): ") or '1'
        sort_by = sort_options.get(sort_choice, 'user_id')
        
        sort_order = input("Sort order (ASC/DESC, default: ASC): ").upper() or 'ASC'
        if sort_order not in ('ASC', 'DESC'):
            sort_order = 'ASC'
        
        while True:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute(
                    "SELECT * FROM get_contacts_paginated(%s, %s, %s, %s)",
                    (page_size, offset, sort_by, sort_order)
                )
                rows = cur.fetchall()
            
            if not rows:
                print("[INFO] No more records found.")
                break
                
            total_count = rows[0]['total_count'] if rows else 0
            total_pages = (total_count + page_size - 1) // page_size
            
            print(f"\n--- Page {page_num} of {total_pages} ---")
            print("ID\tName\t\tPhone")
            print("-" * 40)
            
            for row in rows:
                print(f"{row['user_id']}\t{row['user_name']}\t\t{row['phone_num']}")
                
            print(f"\nShowing records {offset+1}-{min(offset+page_size, total_count)} of {total_count}")
            
            if page_num >= total_pages:
                print("[INFO] End of records.")
                break
                
            choice = input("\nN: Next page, P: Previous page, Q: Quit browsing (N/P/Q): ").upper()
            if choice == 'Q':
                break
            elif choice == 'P' and page_num > 1:
                page_num -= 1
                offset = (page_num - 1) * page_size
            else:  # Default to next page
                page_num += 1
                offset = (page_num - 1) * page_size
                
    except ValueError:
        print("[ERROR] Please enter a valid number.")
    except Exception as e:
        print(f"[ERROR] Pagination query failed: {e}")


# --- PROCEDURE 5: DELETE BY NAME OR PHONE ---

def delete_contact(conn):
    """Delete contact by name or phone using the stored procedure."""
    try:
        print("\nDelete Contact")
        print("1. Delete by name")
        print("2. Delete by phone number")
        
        option = input("Select option: ")
        
        if option == '1':
            value = input("Enter name to delete: ")
            delete_type = 'name'
        elif option == '2':
            value = input("Enter phone number to delete: ")
            delete_type = 'phone'
        else:
            print("[ERROR] Invalid option.")
            return
            
        with conn.cursor() as cur:
            # Change this line to match the parameter order in the procedure definition
            cur.execute("CALL delete_contact(%s, NULL, %s)", (value, delete_type))
            
            # Get the notices with results
            notices = conn.notices
            if notices:
                for notice in notices:
                    print(notice)
                
    except Exception as e:
        print(f"[ERROR] Delete operation failed: {e}")


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


# --- UTILITY FUNCTIONS ---

def view_table_structure(conn):
    """View the structure of the phone_book table."""
    try:
        with conn.cursor() as cur:
            # Get table structure
            cur.execute("""
                SELECT column_name, data_type, character_maximum_length
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE table_name = 'phone_book'
                ORDER BY ordinal_position
            """)
            columns = cur.fetchall()
            
            # Get function and procedure names
            cur.execute("""
                SELECT routine_name, routine_type 
                FROM INFORMATION_SCHEMA.ROUTINES
                WHERE routine_schema = 'public'
                ORDER BY routine_type, routine_name
            """)
            routines = cur.fetchall()
        
        print("\nTable Structure:")
        print("-" * 40)
        for col in columns:
            col_type = col[1]
            if col[2]:  # If has length
                col_type += f"({col[2]})"
            print(f"{col[0]}: {col_type}")
            
        print("\nAvailable Functions and Procedures:")
        print("-" * 40)
        for routine in routines:
            print(f"{routine[1]}: {routine[0]}")
            
    except Exception as e:
        print(f"[ERROR] Failed to retrieve schema: {e}")


def main():
    conn = None
    try:
        # Connect to database and setup
        conn = connect_db()
        setup_database(conn)
        
        menu = {
            # Function 1: Search by pattern
            '1': (search_by_pattern, 'Search contacts by pattern'),
            
            # Procedure 2: Insert or update user
            '2': (upsert_user, 'Insert new user or update existing'),
            
            # Procedure 3: Bulk insert with validation
            '3': (bulk_insert_users, 'Bulk insert users with validation'),
            
            # Function 4: Paginated query
            '4': (paginated_query, 'View contacts with pagination'),
            
            # Procedure 5: Delete by name or phone
            '5': (delete_contact, 'Delete contact by name or phone'),
            
            # Legacy operations
            '6': (insert_from_csv, 'Import from CSV file'),
            
            # Utility
            '7': (view_table_structure, 'View database structure'),
            
            '0': (None, 'Exit')
        }

        while True:
            print("\n" + "=" * 50)
            print("        PHONE BOOK MANAGEMENT SYSTEM")
            print("=" * 50)
            
            # Display menu
            print("\nAVAILABLE OPERATIONS:")
            for key, (_, desc) in menu.items():
                print(f"{key}. {desc}")
            
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