import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SQLiteDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.con = sqlite3.connect(db_name)
        self.con.row_factory = dict_factory
        self.cur = self.con.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.commit()
        self.con.close()

    def sql_query(self, query):
        answer = self.cur.execute(query)
        return answer.fetchall()

    def insert_into(self, table_name, params):
        values = ', '.join([f'"{str(i)}"' for i in params.values()])
        columns = ', '.join(params.keys())

        self.cur.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")

    def select_from(self, table_name: object, columns: list, where: object = None) -> object:
        columns = ', '.join(columns)

        query = f'SELECT {columns} FROM {table_name}'

        if where:
            where = ', '.join([f"{key}='{value}'" for key, value in where.items()])
            query += f' WHERE {where}'

        return self.sql_query(query)