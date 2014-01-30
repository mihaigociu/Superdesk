'''
Created on Jan 27, 2014

@package: workflow
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Gociu

Contains the SQL alchemy meta for assignment API.

'''
from ..api.assignment import Assignment

from sqlalchemy.schema import Column
from sqlalchemy.types import String
from sqlalchemy.dialects.mysql.base import INTEGER
from .metadata_workflow import Base

# --------------------------------------------------------------------

class AssignmentMapped(Base, Assignment):
    '''
    Provides the mapping for Assignment entity.
    '''
    __tablename__ = 'workflow_assignment'
    __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')

    
    Name = Column('name', String(250), nullable=False, unique=True)
    Description = Column('description', String(250), nullable=False, unique=True)
    Node = Column('node_id', INTEGER(unsigned=True), nullable=True)
    # Non REST model attribute --------------------------------------
    id = Column('id', INTEGER(unsigned=True), primary_key=True)

class NodeDB(Base):
    '''
    Provides the mapping for Node entity.
    '''
    __tablename__ = 'workflow_node'
    __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')

    id = Column('id', INTEGER(unsigned=True), primary_key=True)
    GUID = Column('GUID', String(250), nullable=False, unique=True)

# class AssignmentNode(Base):
#     '''
#     '''
#     __tablename__ = 'workflow_assignment_node'
#     __table_args__ = dict(mysql_engine='InnoDB', mysql_charset='utf8')
# 
#     assignment = Column('fk_assignment_id', ForeignKey(AssignmentMapped.id), nullable=False, primary_key=True)
#     node = Column('fk_node_id', ForeignKey(NodeDB.id), nullable=False, primary_key=True)
    