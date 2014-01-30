'''
Created on Jan 27, 2014

@package: workflow
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Gociu

API specifications for Assignment service.

'''

from ally.api.config import service, query, call, UPDATE
from ally.api.criteria import AsLike
from ally.support.api.entity_named import IEntityService, Entity, QEntity
from workflow.api.domain_workflow import modelWorkFlow
from ally.api.option import SliceAndTotal  # @UnusedImport
from ally.api.type import Iter
from workflow.api.nodes import Node

# --------------------------------------------------------------------
@modelWorkFlow
class Assignment(Entity):
    '''
    Provides the assignment model.
    '''
    Name = str
    Description = str
    
# --------------------------------------------------------------------

@query(Assignment)
class QAssignment(QEntity):
    '''
    Provides the query for assignment model.
    '''
    name = AsLike
    description = AsLike
    
# --------------------------------------------------------------------

@service((Entity, Assignment), (QEntity, QAssignment))
class IAssignmentService(IEntityService):
    '''
    Provides the service methods for assignments.
    '''
    
    @call(method=UPDATE)
    def moveAssignmentToNode(self, assignment:Assignment.Name, node:Node.GUID) -> bool:
        ''' '''
    
    @call
    def getNodeForAssignment(self, assignment:Assignment.Name) -> Node:
        ''' '''
    
    @call
    def getAssignmentsForNode(self, node:Node.GUID) -> Iter(Assignment):
        ''' '''
    
