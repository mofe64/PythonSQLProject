from Connection import Connection


class Operation:
    def __init__(self):
        self.__connection = Connection()

    def perform_query_single(self, query: str) -> tuple:
        conn = self.__connection.initialize_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        query_result = cursor.fetchone()
        self.__connection.close_connection()
        return query_result

    def perform_group_query(self, query: str) -> list:
        conn = self.__connection.initialize_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        query_results = cursor.fetchall()
        self.__connection.close_connection()
        return query_results

    def perform_insert(self, insert_statement: str, values: tuple) -> None:
        conn = self.__connection.initialize_connection()
        cursor = conn.cursor()
        cursor.execute(insert_statement, values)
        conn.commit()
        cursor.close()
        self.__connection.close_connection()

    def perform_update(self, update_statement: str, values: tuple) -> None:
        conn = self.__connection.initialize_connection()
        cursor = conn.cursor()
        cursor.execute(update_statement, values)
        conn.commit()
        self.__connection.close_connection()

    def perform_delete(self, delete_statement: str, values: tuple) -> None:
        conn = self.__connection.initialize_connection()
        cursor = conn.cursor()
        cursor.execute(delete_statement, values)
        conn.commit()
        self.__connection.close_connection()
