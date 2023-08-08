import ckan.model as model

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import types
from sqlalchemy import func
from ckan.model.meta import metadata
from ckan.model.types import make_uuid

#Schema of comment table. 
dashboards_table = Table('dashboards_table', metadata, 
    Column('dashboard_Id', types.UnicodeText, primary_key=True, default=make_uuid),
    Column('dashboard_Type_Id', types.UnicodeText),
    Column('dashboard_Arns', types.JSON),
    Column('SME', types.UnicodeText),
    Column('user_Id', types.UnicodeText),
    Column('state', types.UnicodeText)
)

class dashboard(model.DomainObject):

    # Allows for data to be queried 
    def __getitem__(self, field):
        return self.__dict__[field]

    @classmethod
    def get(cls, **kw):
        query = model.Session.query(cls).autoflush(False)
        return query.filter_by(**kw).all()

    @classmethod
    def get_all(cls, **kq):
        query = model.Session.query(cls).all()
        return query
    
    @classmethod
    def find(cls, **kw):
        query = model.Session(cls).autoflush(False)
        return query.filter_by(**kw)
        
model.meta.mapper(dashboard, dashboards_table)