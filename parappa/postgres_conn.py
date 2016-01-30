from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


class DatabaseConnector:

    def __init__(self, db_username, db_password, db_host, db_name, fname, st):
        engine = self.__connect_sql(db_username, db_password, db_host, db_name)
        self.__load_data(engine, fname, st)

############################# PRIVATE FUNCTIONS  ###############################

    def __load_data(self, engine, filename, state):
        if filename == 'apwide.csv':
            table = 'reported_x_candidate_votes'
            psql_copy = "COPY {}.{} FROM STDIN WITH CSV".format(state, table)
        else:
            table = 'reported_votes'
            psql_copy = "COPY {}.{} FROM STDIN WITH CSV HEADER".format(state, table)

        connect = engine.connect()
        connect = engine.connect()
        transaction = connect.begin()
        connect.execute('TRUNCATE TABLE {}.{};'.format(state, table))
        transaction.commit()

        ses = sessionmaker(bind=engine)
        dbcopy_f = open(filename,'r')

        conn = engine.raw_connection()
        cur = conn.cursor()
        cur.copy_expert(psql_copy,dbcopy_f)
        conn.commit()
        ses.close_all()

        if filename == 'apwide.csv':
            os.remove(filename)
        else:
            pass

    def __connect_sql(self, db_username, db_password, db_host, db_name):
        engine = create_engine(
                    'postgresql://{}:{}@{}:5432/{}'.format(db_username,
                                                            db_password,
                                                            db_host,
                                                            db_name
                                                        )
                )

        return engine
