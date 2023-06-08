import sqlite3


def init_db():
    try:
        conn = sqlite3.connect('bot.db')
        cur = conn.cursor()

        with open("create_db.sql", "r") as f:
            sql = f.read()
        cur.executescript(sql)
        conn.commit()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if conn:
            conn.close()


def add_chat(line_id: int, name: str):
    try:
        conn = sqlite3.connect('bot.db')
        cur = conn.cursor()

        insert_message = """INSERT INTO chats VALUES (?, ?);"""

        data = (line_id, name)
        cur.execute(insert_message, data)
        conn.commit()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if conn:
            conn.close()


def add_user(user_id: int, chat_id, user_name: str):
    try:
        conn = sqlite3.connect('bot.db')
        cur = conn.cursor()

        insert_message = """INSERT INTO users VALUES (?, ?, ?);"""

        data = (user_id, chat_id, user_name)
        cur.execute(insert_message, data)
        conn.commit()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if conn:
            conn.close()


def delete_chat(chat_id: int):
    try:
        conn = sqlite3.connect('bot.db')
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM chats WHERE id='{chat_id}'".format(
                chat_id=chat_id
            )
        )
        conn.commit()

        cur.execute(
            "DELETE FROM users WHERE chat_id='{chat_id}'".format(
                chat_id=chat_id
            )
        )
        conn.commit()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if conn:
            conn.close()


def delete_user(user_id: int, chat_id: int):
    try:
        conn = sqlite3.connect('bot.db')
        cur = conn.cursor()

        cur.execute(
            "DELETE FROM users WHERE user_id='{user_id}' AND chat_id='{chat_id}'".format(
                user_id=user_id,
                chat_id=chat_id
            )
        )
        conn.commit()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if conn:
            conn.close()


def get_table(table: str):
    try:
        conn = sqlite3.connect('bot.db')
        cur = conn.cursor()

        cur.execute("""SELECT * FROM {table}""".format(table=table))
        records = cur.fetchall()

        cur.close()
        conn.close()

        return records

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if conn:
            conn.close()


def get_users(chat_id: int):
    try:
        conn = sqlite3.connect('bot.db')
        cur = conn.cursor()

        cur.execute(
            """SELECT user_name FROM users WHERE chat_id={chat_id}""".format(
                chat_id=chat_id
            )
        )
        records = cur.fetchall()

        cur.close()
        conn.close()

        return list(set([i[0] for i in records]))

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if conn:
            conn.close()
