from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseConnector:

    def connect_sql(self):
        engine = create_engine(
                    'postgresql://junto:{}@minas-morgul.cvncnjbhlgez.us-east-1.rds.amazonaws.com:5432/election-day'.format(self.db_password)
                )

        return engine
