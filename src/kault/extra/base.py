from os import path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Session

from ..modules.carry import global_scope

extra_sessions = {}

@as_declarative()
class ExtraBase(object):
    """
        Declarative extra base, shared with all models
    """

    pass


def get_extra_session(fresh=False):
    """
        Return SQLAlchemy session
    """

    global extra_sessions
    if global_scope['extra_db_file'] is None:
        raise RuntimeError("`extra_db_file` is not defined in the global scope")

    # Create a unique key for the db session
    db_file = global_scope['extra_db_file']

    # Add a session to the current list
    if fresh or not extra_sessions.get(db_file):
        extra_sessions[db_file] = Session(bind=get_extra_engine())

    return extra_sessions[db_file]


def drop_extra_sessions():
    """
        Drop current db sessions
    """

    global extra_sessions

    extra_sessions = {}

    return True

def get_extra_engine():
    """
        Return SQLAlchemy engine
    """

    if global_scope['extra_db_file'] is None:
        raise RuntimeError("`extra_db_file` is not defined in the global scope")

    return create_engine(f"sqlite:{get_extra_slashes()}{global_scope['extra_db_file']}") 


def get_extra_slashes():
    """
        Return the appropriate number of slash for the database connection
        based on whether the db path is relative or absolute
    """

    if global_scope['extra_db_file'] is not None and path.isabs(global_scope['extra_db_file']):
        return '////'

    return '///'
