'''
Created on Jan 9, 2012

@@package: development support
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the services for the development support.
'''

from ..ally_core.converter import converterPath
from ..ally_core.resource_management import resourcesRegister, services
from ally.container import ioc
from development.request.api.request import IRequestService
from development.request.impl.request import RequestService

# --------------------------------------------------------------------

@ioc.config
def publish_development():
    '''
    If true the development services will be published.
    '''
    return True

@ioc.entity
def requestService() -> IRequestService:
    b = RequestService(); yield b
    b.resourcesRegister = resourcesRegister()
    b.converterPath = converterPath()


# --------------------------------------------------------------------

@ioc.before(services)
def publishServices():
    if publish_development():
        services().append(requestService())
