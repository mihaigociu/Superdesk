'''
Created on Jan 9, 2012

@package: workflow
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the services for workflow.
'''

from ..plugin.registry import registerService
from .database import binders
from ally.container import support, bind, ioc

# --------------------------------------------------------------------

SERVICES = 'workflow.api.**.I*Service'

bind.bindToEntities('workflow.impl.**.*Alchemy', binders=binders)
support.createEntitySetup('workflow.impl.**.*')
support.listenToEntities(SERVICES, listeners=registerService)
support.loadAllEntities(SERVICES)

# --------------------------------------------------------------------

@ioc.entity
def workflows() -> list: return ['Copy Tasting']