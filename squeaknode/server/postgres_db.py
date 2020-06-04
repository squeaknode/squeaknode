import psycopg2


class PostgresDb():

    def __init__(self, params):
        self.params = params

    def get_connection(self):
        """ Connect to the PostgreSQL database server """
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as curs:
	        # execute a statement
                print('PostgreSQL database version:')
                curs.execute('SELECT version()')

                # display the PostgreSQL database server version
                db_version = curs.fetchone()
                print(db_version)
