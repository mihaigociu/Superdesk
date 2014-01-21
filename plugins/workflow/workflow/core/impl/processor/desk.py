'''
Created on Jan 15, 2014

@package: workflow
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Gociu

Manages Desk nodes creation.

'''

from ally.container.ioc import injected
from ally.design.processor.attribute import defines
from ally.design.processor.context import Context
from ally.design.processor.execution import Chain
from ally.design.processor.handler import HandlerProcessor
import logging
from ally.container import wire
from workflow.api.desk import IDeskService

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class WorkFlow(Context):
    nodes = defines(dict, doc='''
    @rtype: dict
    Mapps Node.GUID : Node
    ''')

class NodeDesk(Context):
    GUID = defines(str, doc='''
    @rtype: str
    The guid of the node
    ''')
    name = defines(str, doc='''
    @rtype: str
    The name of the node (should be unique too).
    ''')
    allowUsers = defines(bool, doc='''
    @rtype: bool
    guess what this is for
    ''')
    edges = defines(list, doc='''
    @rtype: list
    List of edges.
    ''')

class EdgeDesk(Context):
    defaultAction = defines(str, doc='''
    @rtype: dict
    just read the bloody name of the attribute
    ''')
    destination = defines(Context, doc='''
    @rtype: dict
    same as above
    ''')

# --------------------------------------------------------------------

@injected
class DeskHandler(HandlerProcessor):
    '''
    Implementation for a processor that creates Desk nodes.
    '''
    
    deskService = IDeskService; wire.entity('deskService')
    # TODO: config defaultAction
    
    def __init__(self):
        assert isinstance(self.deskService, IDeskService), 'Invalid desk service %s' % self.deskService
        super().__init__()
    
    def process(self, chain, workFlow:WorkFlow, Node:NodeDesk, Edge:EdgeDesk,  **keyargs):
        '''
        @see: HandlerProcessor.process
        '''
        assert isinstance(chain, Chain), 'Invalid chain %s' % chain
        assert isinstance(workFlow, WorkFlow), 'Invalid work flow %s' % workFlow
        
        #build nodes repository
        desksDb = self.deskService.getAll()
        if not workFlow.nodes: workFlow.nodes = {}

        for name in desksDb:
            workFlow.nodes[name] = Node(name = name)
            
        #for each desk node create the connections with other desk nodes
        for node in workFlow.nodes.values():
            assert isinstance(node, Node), 'Invalid node %s' % node
            connections = self.deskService.getDestinations(node.name)
            if not node.edges: node.edges = []
            for deskName in connections:
                destination = workFlow.nodes.get(deskName, None)
                if destination: node.edges.append(Edge(defaultAction='move', destination=destination))
                
