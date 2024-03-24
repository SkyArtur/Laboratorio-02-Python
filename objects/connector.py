import psycopg2
from functions import reader


class Connector:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance or cls.__instance is None:
            cls.__instance = super(Connector, cls).__new__(cls)
        return cls.__instance

    def __init__(self, *args, **kwargs):
        self.__conn = None
        self.__cursor = None
        self.__response = None

    def execute(self, query: str, data: tuple = None, fetchone: bool = False) -> tuple:
        """
        Executa a query e retorna o resultado da consulta.
        :param query: consulta SQL.
        :param data: dados pra a consulta ou registro.
        :param fetchone: retornar único valor da consulta.
        :return: tupla de resultados da consulta.
        """
        try:
            self.__conn = psycopg2.connect(**reader('params.json'))
            self.__cursor = self.__conn.cursor()
            self.__cursor.execute(query, data)
            self.__response = self.__cursor.fetchall() if not fetchone else self.__cursor.fetchone()
        except (TypeError, psycopg2.DatabaseError) as error:
            print(f'Error while connecting to PostgreSQL: {error}')
        else:
            self.__conn.commit()
            return self.__response
        finally:
            self.__cursor.close()
            self.__conn.close()
