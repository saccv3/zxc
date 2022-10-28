import psycopg2


# class for create connect to database, a little api.. :))))
class DatabaseConnection:
    __connection = ''

    # init method was creating connect to database
    def __init__(self, host, user, password, db_name):
        self.__connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        self.__connection.autocommit = True

        print("[INFO] PostgresSQL подключение к базе данных установлено ")

    # method for a put some data into data table
    def put_data_user_table(self, *args):
        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO bot_users(phone_number, chat_id) values(%s, %s);",
                (
                    args[0]['user_phone_contact'],
                    str(args[0]['user_chat_id'])
                 )
            )
            print('[INFO] Данные занесены в таблицу')

        return True # return True To understand the correct data entry

    # method delete some rows
    def drop_data_into_tables(self, chat_id):
        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"DELETE FROM bot_users WHERE chat_id='{chat_id}';",
            )

            print(f'[INFO] Данные пользователя chat_id={chat_id}, были удалены')

    # method for a checked correctable email adress
    def condition_data_put(self, some_email):
        with self.__connection.cursor() as cursor:
            cursor.execute(
                "SELECT email_user FROM bot_users;"
            )

            for el in cursor.fetchall():
                if some_email.find('@') == -1:
                    print(f"[INFO] {some_email} это не почта! \n")
                    return False
                elif some_email == el[0]:
                    print("[INFO] Ваша почта уже используется \n")
                    return False
            else:
                print(f'[INFO] Ваша почта введена корректно \n')
                return True

    # method for a get database tables, use args
    def get_table_content(self, *args):
        with self.__connection.cursor() as cursor:
            text = ' ,'.join(args)
            cursor.execute(
                f"SELECT {text if len(text) > 0 else text.__add__('*')} FROM bot_users;"
            )
            print(cursor.fetchall())
            return cursor.fetchall()

    def find_table_content(self, chat_id):
        found = True
        with self.__connection.cursor() as cursor:
            # text = ' ,'.join(args)
            cursor.execute(
                f"SELECT * FROM bot_users WHERE chat_id='{chat_id}';"
            )
            found = not cursor.fetchall()
            print(f'[INFO] Данные пользователя {chat_id}, успешно найдены.')

        print(found)
        return not found

    def mailing_start(self):
        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"SELECT chat_id FROM bot_users WHERE send_inform='True'"
            )
            return cursor.fetchall()

    def update_data(self, chat_id):
        data = False
        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"SELECT send_inform FROM bot_users WHERE chat_id='{chat_id}'"
            )

            data = cursor.fetchone()

        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE bot_users SET send_inform = {not data[0]} WHERE chat_id='{chat_id}'"
            )
            print(f'[INFO] Рассылка для пользователя chat_id={chat_id}, теперь {not data[0]}')

        return not data[0]

    # method return version PostgresDataBase
    def get_version(self):
        with self.__connection.cursor() as cursor:
            cursor.execute(
                "SELECT version();"
            )
            print(f'{cursor.fetchone()}')
            return cursor.fetchone()

    # method return object connection
    def get_connection(self):
        return self.__connection

    # method for a close a connection
    def close_connection(self):
        if self.__connection:
            self.__connection.close()
            print('[INFO] PostgresSQL подключение закрыто. \n')
