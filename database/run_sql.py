# Módulo de conexão ao banco de dados

# pip install psycopg2
# https://pypi.org/project/psycopg2/

# Imports
# import os
import psycopg2
import psycopg2.extras as ext

def run_sql(sql, values = None):

    # Variáveis de controle
    connection = None
    results = []

    # Conexão ao banco de dados
    try:
        connection = psycopg2.connect("host=localhost port=5432 dbname=databaseapp user=postgres password=academy")
        cursor = connection.cursor(cursor_factory= ext.DictCursor)
        cursor.execute(sql, values)
        connection.commit()
        results = cursor.fetchall()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
    return results