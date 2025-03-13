import sqlalchemy as sqa
import pandas as pd
from optigob.database import get_local_dir
import os


class DatabaseManager:
    def __init__(self, database_path=None):
        """
        Initializes the DataManager class.
        
        Parameters:
            database_path (str, optional): Path to the SQLite database file. 
                                           If None, uses the default database located in the local directory.
        """
        if database_path is None:
            self.database_dir = get_local_dir()
            self.database_path = os.path.abspath(
                os.path.join(self.database_dir, "optigob_default.db")
            )
        else:
            self.database_path = os.path.abspath(database_path)
            
        self.engine = self.create_engine()

    def create_engine(self):
        """
        Creates a SQLAlchemy engine connected to the SQLite database specified by self.database_path.
        
        Returns:
            sqlalchemy.engine.Engine: A SQLAlchemy engine instance connected to the specified SQLite database.
        """
        engine_url = f"sqlite:///{self.database_path}"
        return sqa.create_engine(engine_url)


    def get_livestock_scalers(self):
        """
        """
        table = "animal_scalers"
        dataframe = pd.read_sql(
            "SELECT * FROM '%s'" % (table),
            self.engine,
        )
        return dataframe
