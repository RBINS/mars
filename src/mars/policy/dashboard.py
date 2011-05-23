from zope.interface import implements
from zope.component import adapts
from interfaces import IMyPortalUser
from plone.app.portlets.interfaces import IDefaultDashboard
from plone.app.portlets.dashboard import DefaultDashboard
from plone.app.portlets import portlets

class MyPortalDefaultDashboard(DefaultDashboard):
    """ A new custom default dashboard for users. """
    implements(IDefaultDashboard)
    adapts(IMyPortalUser)

    def __call__(self):
        news = portlets.news.Assignment()
        recent = portlets.recent.Assignment()
        calendar = portlets.calendar.Assignment()
        search = portlets.search.Assignment()

        return {
            'plone.dashboard1' : (news,),
            'plone.dashboard2' : (calendar,),
            'plone.dashboard3' : (recent,),
            'plone.dashboard4' : (search,),
        }