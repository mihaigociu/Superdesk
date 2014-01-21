'''
Created on Jan 17, 2012

@package: workflow
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the database settings.
'''

from ..sql_alchemy.db_application import metas, bindApplicationSession
from ally.container import ioc
from workflow.meta.metadata_workflow import meta

# --------------------------------------------------------------------

@ioc.entity
def binders(): return [bindApplicationSession]

# --------------------------------------------------------------------

@ioc.before(metas)
def updateMetasForSuperdesk(): metas().append(meta)
