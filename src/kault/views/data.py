from ..extra.base import get_extra_session
from ..extra.Data import DataModel

def all():
    return get_extra_session().query(DataModel).order_by(DataModel.id).all()

def add(id, name, url='', login='', password='', notes='', category=''):
    """
        Create a new secret
    """
 
    data = DataModel(id=id,
                     name=name,
                     url=url,
                     login=login,
                     password=password,
                     notes=notes,
                     category=category)
    get_extra_session().add(data)
    get_extra_session().commit()

    return True


def delete(id_):

    data = get_extra_session().query(DataModel).filter(
        DataModel.id == int(id_)).first()

    if data:
        get_extra_session().delete(data)
        get_extra_session().commit()

        return True

    return False

def search(query):
    """
        Search by keyword
    """

    query = '%' + str(query) + '%'

    return get_extra_session().query(DataModel) \
        .filter(or_(DataModel.name.like(query), DataModel.url.like(query), DataModel.login.like(query))) \
        .order_by(DataModel.id).all()
