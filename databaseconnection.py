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

        print("[INFO] PostgresSQL connection was activate ")

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
            print('[INFO] DATA PUT INTO DATABASE')

        return True # return True To understand the correct data entry

    # method delete some rows
    def drop_data_into_tables(self, chat_id):
        with self.__connection.cursor() as cursor:
            cursor.execute(
                f"DELETE FROM bot_users WHERE chat_id='{chat_id}';",
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
        boola = True
        with self.__connection.cursor() as cursor:
            # text = ' ,'.join(args)
            cursor.execute(
                f"SELECT * FROM bot_users WHERE chat_id='{chat_id}';"
            )
            boola = not cursor.fetchall()
            print('[INFO] Data successfully found')

        print(boola)
        return not (boola)

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
            print('[INFO] PostgresSQL connection closed \n')
