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
from ally.design.processor.execution import Processing, FILL_ALL
from ally.design.processor.handler import Handler, HandlerBranching
import logging
from ally.container import wire
from workflow.api.desk import IDeskService
from workflow.api.desk_user_workflow import IDeskUserWorkflowService
from ally.container.support import setup
from workflow.api import nodes
from ally.design.processor.assembly import Assembly
from ally.design.processor.branch import Branch

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------

class Graph(Context):
    nodes = defines(dict, doc='''
    @rtype: dict
    Mapps Node.GUID : Node
    ''')

class NodeDesk(Context):
    ''' The node context.'''
    model = defines(nodes.Node, doc='''
    @rtype: Node
    The node model associated with the node context.
    ''')
    edges = defines(list, doc='''
    @rtype: list
    List of edges.
    ''')
    workflow = defines(Context, doc='''
    @rtype: NodeDesk
    The workflow for this desk.
    ''')

class EdgeDesk(Context):
    model = defines(nodes.Edge, doc='''
    @rtype: Edge
    The edge model associated with the edge context.
    ''')

class GraphWorkflow(Context):
    ''' Provides the graph for a desk.'''
    input = defines(Context)
    output = defines(Context)
    workflows = defines(set, doc='''
    @rtype: set(string)
    list of workflows.
    ''')
    
# --------------------------------------------------------------------

@injected
@setup(Handler, name='deskHandler')
class DeskHandler(HandlerBranching):
    '''
    Implementation for a processor that creates Desk nodes.
    '''
    
    deskService = IDeskService; wire.entity('deskService')
    deskUserWorkflowService = IDeskUserWorkflowService; wire.entity('deskUserWorkflowService')
    # TODO: config defaultAction
    assemblyWorkflow = Assembly; wire.entity('assemblyWorkflow')
    
    def __init__(self):
        assert isinstance(self.deskService, IDeskService), 'Invalid desk service %s' % self.deskService
        assert isinstance(self.deskUserWorkflowService, IDeskUserWorkflowService), \
        'Invalid desk_user_workflow service %s' % self.deskUserWorkflowService
        assert isinstance(self.assemblyWorkflow, Assembly), 'Invalid assembly %s' % self.assemblyWorkflow
        super().__init__(Branch(self.assemblyWorkflow).using(graphWorkflow=GraphWorkflow).included())
    
    def process(self, chain, processing, graph:Graph, Node:NodeDesk, Edge:EdgeDesk, **keyargs):
        '''
        @see: HandlerProcessor.process
        '''
        assert isinstance(graph, Graph), 'Invalid work flow %s' % graph
        
        #build nodes repository
        desksDb = self.deskService.getAll()
        if not graph.nodes: graph.nodes = {}

        for name in desksDb:
            graph.nodes[name] = Node(model=nodes.Node(name, name))
            
        #for each desk node create the connections with other desk nodes
        nodeIds = [nodeId for nodeId in graph.nodes.keys()]
        for nodeId in nodeIds:
            node = graph.nodes.get(nodeId)
            assert isinstance(node, NodeDesk), 'Invalid node %s' % node
            
            connections = self.deskService.getDestinations(node.model.Name)
            if not node.edges: node.edges = []
            for deskName in connections:
                destination = graph.nodes.get(deskName, None)
                if destination: node.edges.append(Edge(model=nodes.Edge(destination.model.GUID, 'move')))

            workflows = set(self.deskUserWorkflowService.getWorkflows(node.model.Name))            
            assert isinstance(processing, Processing), 'Invalid processing %s' % processing
            node.workflow = Node(model=nodes.Node(node.model.GUID, node.model.Name))
            graphWorkflow = processing.ctx.graphWorkflow(input=node.workflow, output=node.workflow, workflows=workflows)
            arg = processing.execute(FILL_ALL, graphWorkflow=graphWorkflow, graph=graph, Node=Node, Edge=Edge, **keyargs)
            arg
            
            
            
            