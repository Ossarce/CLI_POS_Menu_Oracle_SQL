
def fetch_users(connection, users):
    cursor = connection.cursor()

    query = 'SELECT * FROM USERS'
    cursor.execute(query)
    for row in cursor.fetchall():
        print(row)

        user = {
            'username': row[1],
            'password': row[2],
        }

        users.append(user)

    cursor.close()

    return users

def insert_user(connection, user):
    cursor = connection.cursor()

    existing_query = 'SELECT COUNT(*) FROM USERS WHERE username = :username'
    cursor.execute(existing_query, username = user['username'])
    count = cursor.fetchone()[0]

    if count == 0:
        insert_query = 'INSERT INTO USERS (username, password) VALUES (:username, :password)'

        cursor.execute(insert_query, username = user['username'], password = user['password'])
        
        print('El usuario:', user['username'], 'ha sido agregado a la base de datos')
    else:
        print('El usuario:', user['username'], 'ya existe en la base de datos')

    connection.commit()

    cursor.close()