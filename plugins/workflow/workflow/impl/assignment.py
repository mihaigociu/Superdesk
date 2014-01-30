'''
Created on Jan 27, 2014

@package: workflow
@copyright: 2011 Sourcefabric o.p.s.
@license http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Gociu

Implementation for assignment service.

'''
from ally.container.ioc import injected
from ally.container.support import setup
from sql_alchemy.impl.entity import EntityServiceAlchemy
from ally.api.validate import validate
from sqlalchemy.orm.exc import NoResultFound
from workflow.api.assignment import IAssignmentService, QAssignment, Assignment
from workflow.meta.assignment import AssignmentMapped, NodeDB
from ally.container import wire
from workflow.api.nodes import INodesService
from workflow.api.nodes import Node

# --------------------------------------------------------------------

@injected
@setup(IAssignmentService, name='assignmentService')
@validate(AssignmentMapped)
class AssignmentServiceAlchemy(EntityServiceAlchemy, IAssignmentService):
    '''
    Implementation for @see: IAssignmentService
    '''
    nodesService = INodesService; wire.entity('nodesService')
    
    def __init__(self):
        EntityServiceAlchemy.__init__(self, AssignmentMapped, QAssignment)
    
    def moveAssignmentToNode(self, assignment, node):
        '''
        @see: IAssignmentService.moveAssignmentToNode 
        '''
        #check if the node is in the Graph
        if not self.nodesService.getNode(node):
            self.removeNodeFromDB(node)
            return False
        
        #check if the assignment exists
        try:
            assignmentMapped = self.session().query(AssignmentMapped).filter(AssignmentMapped.Name == assignment).one()
        except NoResultFound: return False
        
        #add the node to database, if it is not already there
        try:
            self.session().query(NodeDB.id).filter(NodeDB.GUID == node).one()
        except NoResultFound:
            nodeDB = NodeDB()
            nodeDB.GUID = node
            self.session().add(nodeDB)
        
        #make sure the assignment is not already on the node
        sql = self.session().query(AssignmentMapped.Node).join(NodeDB, NodeDB.id == AssignmentMapped.Node)
        sql = sql.filter((AssignmentMapped.Name == assignment) & (NodeDB.GUID == node))
        if sql.count() > 0: return True
        
        #change the current location of the assignment
        nodeId, = self.session().query(NodeDB.id).filter(NodeDB.GUID == node).one()
        assert isinstance(assignmentMapped, AssignmentMapped), 'Invalid assignment %s' % assignmentMapped
        assignmentMapped.Node = nodeId
        self.session().add(assignmentMapped)
        return True
    
    def getUnassignedAssignments(self):
        #get the assignments with invalid node or with no node
        sql = self.session().query(AssignmentMapped, NodeDB.GUID).outerjoin(NodeDB, NodeDB.id == AssignmentMapped.Node)
        return [assignment for assignment, node in sql.all() if not self.nodesService.getNode(node)]
    
    def getNodeForAssignment(self, assignment):
        '''
        @see: IAssignmentService.getNodeForAssignment
        '''
        sql = self.session().query(NodeDB.GUID).join(NodeDB, NodeDB.id == AssignmentMapped.Node)
        sql = sql.filter((AssignmentMapped.Name == assignment))
        try:
            node, = sql.one()
            if not self.nodesService.getNode(node):
                self.removeNodeFromDB(node)
                return None
            return node
        except NoResultFound:
            return None
        
    def getAssignmentsForNode(self, node):
        '''
        @see: IAssignmentService.getAssignmentsForNode
        '''
        if not self.nodesService.getNode(node):
            self.removeNodeFromDB(node)
            return []
        
        sql = self.session().query(AssignmentMapped).join(NodeDB, NodeDB.id == AssignmentMapped.Node)
        sql = sql.filter(NodeDB.GUID == node)
        
        assignments = []
        for mapped in sql.all():
            assignment = Assignment()
            assignment.Name = mapped.Name
            assignment.Description = mapped.Description
            assignment.Node = node
            assignments.append(mapped)
        
        return assignments
    
    def removeNodeFromDB(self, node):
        #do some cleanup on the database: delete the node from the database
        try:
            nodeDB = self.session().query(NodeDB).filter(NodeDB.GUID == node).one()
        except NoResultFound: return
        self.session().delete(nodeDB)
        
    #TODO: will not use this for now so DELETE it
    def syncNodesWithDb(self):
        ''' '''
        nodes = self.nodesService.getNodes()
        nodesFromGraph = {node.GUID for node in nodes}
        nodesFromDb = {guid for guid in self.session().query(NodeDB.GUID).all()}
        
        toAdd = nodesFromGraph.difference(nodesFromDb)
        toDelete = nodesFromDb.difference(nodesFromGraph)
        
        for node in nodes:
            assert isinstance(node, Node), 'Invalid node %s' % node
            
            nodeMapped = NodeDB()
            nodeMapped.GUID = node.GUID
            
            #test to see if this really works
            if node.GUID in toAdd:
                self.session().add(nodeMapped)
            elif node.GUID in toDelete:
                self.session().delete(node)
            
    
        
    
        
