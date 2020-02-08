from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class AlchemyManager:
    def __init__(self, db_location):
        self.base = declarative_base()
        self.engine = create_engine(db_location)
        self.dbsession = None
        self.session = None

        self.columns = []

    def start(self):
        self.base.metadata.create_all(self.engine)
        self.base.metadata.bind = self.engine
        self.dbsession = sessionmaker(bind=self.engine)
        self.session = self.dbsession()
