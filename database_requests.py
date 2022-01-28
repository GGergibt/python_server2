from dotenv import dotenv_values
import dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

config = dict(dotenv.dotenv_values(".env"))
password = next(iter(config.values()))
connection_to_database = psycopg2.connect(
    host="localhost", database="personal_chat_history", user="www", password=password
)
connection_to_database.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection_to_database.cursor()
def insert_account_in_database_if_not_exists(cursor, chat_id: int, account: str, profiles_column: str)-> bool:
    """insert in user_table user''s chat_id if not exists and insta/tiktok profiles if not exists. If exists return False, else return True. Account : profile which need to save, profiles_colum : name of column where account need to save, can be insta/tt accounts. Chat_id : user''s ID. download_count : count user''s download """
    sql_selecting = f"SELECT MAX(download_count) FROM user_table WHERE chat_id = {chat_id} AND {profiles_column} = '{account}'"
    execute_command = cursor.execute(sql_selecting)
    write_answer = cursor.fetchall()
    for every_answer in write_answer[0]:
        if every_answer != None:
            download_count = every_answer + 1
        else:
            download_count = 1 
    excepted_answer = [(download_count,)]
    if write_answer == excepted_answer:
        return False
    else:
        print('inserting')
        sql_inserting = f"INSERT INTO user_table(chat_id, {profiles_column}, download_count) VALUES({chat_id}, '{account}', {download_count})"
        inserting_command = cursor.execute(sql_inserting)
        return True
    
def selecting_accounts_if_exists(cursor, chat_id: int, profiles_column: str):
    """Return user''s save profiles if exists, else return False"""
    sql_selecting = f"SELECT {profiles_column} FROM user_table WHERE chat_id = {chat_id} and {profiles_column} != 'null' GROUP BY {profiles_column} ORDER BY MAX(download_count) DESC LIMIT 3"
    execute_command = cursor.execute(sql_selecting)
    write_answer = cursor.fetchall()
    return write_answer

def selecting_download_count_if_exists(cursor, chat_id: int, profiles_column):
    sql_selecting = f"SELECT MAX(download_count) FROM user_table WHERE chat_id = {chat_id} and {profiles_column} != 'null' GROUP BY {profiles_column} ORDER BY MAX(download_count) DESC LIMIT 3"
    # if not write_answer:
    execute_command = cursor.execute(sql_selecting)
    write_answer = cursor.fetchall()
    return write_answer
    # if not write_answer:
        # return False
        # print("hello") 
    # else:


# i = selecting_accounts_if_exists(cursor, 4, 'insta_accounts')
# i = insert_accounts_if_exists(cursor, 4, 'insta_accounts')
# print(i)
