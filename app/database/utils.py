from sqlalchemy import inspect
from wsgi import db

def table_exists(table_name):
    inspector = inspect(db.engine)
    return table_name in inspector.get_table_names()
