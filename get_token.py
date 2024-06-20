import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='moodle'
)

cursor = conn.cursor()

try:

    create_table_query = """
    CREATE TEMPORARY TABLE temp_token (
        userid BIGINT(10),
        secret VARCHAR(1333),
        label VARCHAR(1333)
    )
    """
    cursor.execute(create_table_query)

    insert_query = """
    INSERT INTO temp_token (userid, secret, label)
    SELECT userid, secret, label FROM mdl_tool_mfa WHERE secret IS NOT NULL
    """
    cursor.execute(insert_query)

    update_query = """
    UPDATE temp_token AS tt
    JOIN mdl_tool_mfa AS mfa ON tt.userid = mfa.userid
    SET tt.label = mfa.label
    WHERE mfa.label LIKE '%@gmail.com'
    """
    cursor.execute(update_query)

    select_query = """
    SELECT * FROM temp_token
    """
    cursor.execute(select_query)

    print("Hasil query SELECT:")
    for row in cursor.fetchall():
        print(row)

    drop_table_query = """
    DROP TEMPORARY TABLE temp_token
    """
    cursor.execute(drop_table_query)

    conn.commit()

except mysql.connector.Error as error:
    print("Error:", error)

finally:
    cursor.close()
    conn.close()
