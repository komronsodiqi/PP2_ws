-- This file contains all the SQL functions and procedures for the PhoneBook application
-- Save this as sql_functions.sql in the same directory as your Python script

-- 1. Function that returns all records based on a pattern
CREATE OR REPLACE FUNCTION find_contacts_by_pattern(search_pattern TEXT)
RETURNS TABLE (
    user_id INT,
    user_name VARCHAR(150),
    phone_num VARCHAR(15)
) AS $$
BEGIN
    RETURN QUERY
    SELECT pb.user_id, pb.user_name, pb.phone_num
    FROM phone_book pb
    WHERE 
        pb.user_name ILIKE '%' || search_pattern || '%' OR
        pb.phone_num ILIKE '%' || search_pattern || '%'
    ORDER BY pb.user_id;
END;
$$ LANGUAGE plpgsql;

-- 2. Procedure to insert new user or update phone if user exists
CREATE OR REPLACE PROCEDURE upsert_user(
    p_user_name VARCHAR(150),
    p_phone_num VARCHAR(15)
)
AS $$
DECLARE
    v_exists BOOLEAN;
BEGIN
    -- Check if user exists
    SELECT EXISTS (
        SELECT 1 FROM phone_book WHERE user_name = p_user_name
    ) INTO v_exists;
    
    IF v_exists THEN
        -- User exists, update phone
        UPDATE phone_book
        SET phone_num = p_phone_num
        WHERE user_name = p_user_name;
        
        RAISE NOTICE 'User % already exists. Phone updated to %.', p_user_name, p_phone_num;
    ELSE
        -- User doesn't exist, insert new record
        INSERT INTO phone_book(user_name, phone_num)
        VALUES (p_user_name, p_phone_num);
        
        RAISE NOTICE 'New user % with phone % inserted.', p_user_name, p_phone_num;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- 3. Procedure to insert many users with phone validation
CREATE OR REPLACE PROCEDURE bulk_insert_users(
    p_names TEXT[],
    p_phones TEXT[],
    OUT invalid_entries TEXT[]
)
AS $$
DECLARE
    v_name TEXT;
    v_phone TEXT;
    v_count INT;
    v_phone_pattern TEXT := '^\+?[0-9]{1,3}[-\s]?[0-9]{3,}[-\s0-9]*$'; -- Basic phone validation pattern
    v_invalid_data TEXT;
BEGIN
    -- Initialize output array for invalid entries
    invalid_entries := '{}';
    
    -- Check arrays have same length
    IF array_length(p_names, 1) != array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'Names and phones arrays must have the same length';
    END IF;
    
    -- Process each entry
    v_count := array_length(p_names, 1);
    
    FOR i IN 1..v_count LOOP
        v_name := p_names[i];
        v_phone := p_phones[i];
        
        -- Validate inputs
        IF v_name IS NULL OR length(trim(v_name)) = 0 THEN
            v_invalid_data := 'Entry ' || i || ': Empty name';
            invalid_entries := array_append(invalid_entries, v_invalid_data);
            CONTINUE;
        END IF;
        
        -- Validate phone format using regex
        IF v_phone IS NULL OR NOT v_phone ~ v_phone_pattern THEN
            v_invalid_data := 'Entry ' || i || ': Invalid phone format (' || coalesce(v_phone, 'NULL') || ') for user ' || v_name;
            invalid_entries := array_append(invalid_entries, v_invalid_data);
            CONTINUE;
        END IF;
        
        -- If valid, insert the user
        BEGIN
            CALL upsert_user(v_name, v_phone);
        EXCEPTION WHEN OTHERS THEN
            v_invalid_data := 'Entry ' || i || ': Database error for ' || v_name || ' - ' || SQLERRM;
            invalid_entries := array_append(invalid_entries, v_invalid_data);
        END;
    END LOOP;
    
    -- Report invalid entries
    IF array_length(invalid_entries, 1) > 1 THEN
        FOR i IN 1..array_length(invalid_entries, 1)-1 LOOP
            RAISE NOTICE '%', invalid_entries[i];
        END LOOP;
    END IF;
    
    RAISE NOTICE 'Bulk insert completed. % invalid entries found.', array_length(invalid_entries, 1) - 1;
END;
$$ LANGUAGE plpgsql;

-- 4. Function for paginated queries
CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_limit INT DEFAULT 10,
    p_offset INT DEFAULT 0,
    p_sort_by TEXT DEFAULT 'user_id',
    p_sort_order TEXT DEFAULT 'ASC'
)
RETURNS TABLE (
    user_id INT,
    user_name VARCHAR(150),
    phone_num VARCHAR(15),
    total_count BIGINT
) AS $$
DECLARE
    v_query TEXT;
    v_count BIGINT;
BEGIN
    -- Get total count for pagination info
    SELECT COUNT(*) INTO v_count FROM phone_book;
    
    -- Validate sort parameters to prevent SQL injection
    IF p_sort_by NOT IN ('user_id', 'user_name', 'phone_num') THEN
        p_sort_by := 'user_id';
    END IF;
    
    IF p_sort_order NOT IN ('ASC', 'DESC') THEN
        p_sort_order := 'ASC';
    END IF;
    
    -- Dynamic query with validated parameters
    v_query := format('
        SELECT pb.user_id, pb.user_name, pb.phone_num, %L::BIGINT as total_count
        FROM phone_book pb
        ORDER BY %I %s
        LIMIT %L OFFSET %L',
        v_count, p_sort_by, p_sort_order, p_limit, p_offset
    );
    
    RETURN QUERY EXECUTE v_query;
END;
$$ LANGUAGE plpgsql;

-- 5. Procedure to delete by username or phone
CREATE OR REPLACE PROCEDURE delete_contact(
    p_value        TEXT,
    OUT rows_deleted INT,
    p_type         TEXT DEFAULT 'name'   -- now at the end
)
AS $$
BEGIN
    rows_deleted := 0;

    IF p_type = 'name' THEN
        DELETE FROM phone_book
        WHERE user_name = p_value;
        GET DIAGNOSTICS rows_deleted = ROW_COUNT;
        RAISE NOTICE 'Deleted % record(s) with name: %', rows_deleted, p_value;
    ELSIF p_type = 'phone' THEN
        DELETE FROM phone_book
        WHERE phone_num = p_value;
        GET DIAGNOSTICS rows_deleted = ROW_COUNT;
        RAISE NOTICE 'Deleted % record(s) with phone: %', rows_deleted, p_value;
    ELSE
        RAISE EXCEPTION 'Invalid delete type. Use "name" or "phone".';
    END IF;
END;
$$ LANGUAGE plpgsql;
