import psycopg2


class DatabaseConnection:
    __connection = ''

    def __init__(self, host, user, password, db_name):
        self.__connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        self.__connection.autocommit = True

        print("[INFO] Соединение с базой данных установленно. ")

    def put_data_user_table(self, *args):
        with self.__connection.cursor() as cursor:
            text = ','.join(args)
            cursor.execute(
                f"INSERT INTO bot_users(name_user, email_user, phone_number_user, uniq_chat_id) values(%s, %s, %s, %s);",
                (
                    args[0],
                    args[1],
                    args[2],
                    args[3]
                 )
            )
            print('[INFO] DATA PUT INTO DATABASE')

    def drop_data_into_tables(self, param):
        with self.__connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM user_list WHERE email='%s';", (param)
            )

            print('[INFO] Data into table was dropped')

    # method for a checked correctable email adress
    def condition_data_put(self, some_email):
        with self.__connection.cursor() as cursor:
            cursor.execute(
                "SELECT email_user FROM bot_users;"
            )

            for el in cursor.fetchall():
                if some_email.find('@') == -1:
                    print(f"[INFO] {some_email} that is a not email \n")
                    return False
                elif some_email == el[0]:
                    print("[INFO] your mail already exists \n")
                    return False
            else:
                print(f'[INFO] Your email is correctable \n')
                return True

    # method return object connection
    def get_connection(self):
        return self.__connection

    # method for a close a connection
    def close_connection(self):
        if self.__connection:
            self.__connection.close()
            print('[INFO] PostgresSQL connection closed \n')

    # method for a get database tables, use args
    def get_table_content(self, *args):
        with self.__connection.cursor() as cursor:
            text = ' ,'.join(args[0])
            cursor.execute(
                f"SELECT {text if len(text) > 0 else text.__add__('*')} FROM bot_users;"
            )
            return cursor.fetchall()

    # method return version PostgresDataBase
    def get_version(self):
        with self.__connection.cursor() as cursor:
            cursor.execute(
                "SELECT version();"
            )
            print(f'{cursor.fetchone()}')
            return cursor.fetchone()
