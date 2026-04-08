import mysql.connector


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="example",
        database="testdb"
    )


def find_user(username):
    """
    UNSICHER: Benutzereingabe wird direkt in den SQL-Query eingebaut.
    CodeQL meldet hier: "Query built from user-controlled sources" (SQL-Injection).

    Angriff möglich z.B. mit: username = "' OR '1'='1"
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # CodeQL flaggt diese Zeile: user-controlled data fließt in SQL-Query
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)

    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def find_user_safe(username):
    """
    SICHER: Parameterisierter Query — so sollte es aussehen.
    CodeQL meldet hier nichts.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))

    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


if __name__ == "__main__":
    user_input = input("Username: ")
    print(find_user(user_input))
