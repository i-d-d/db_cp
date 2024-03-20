from settings import settings
import psycopg2

def connect():
    return psycopg2.connect(database=settings.database_name,
                            host=settings.database_host,
                            user=settings.database_user,
                            password=settings.database_password,
                            port=settings.database_port)

connection = connect()
