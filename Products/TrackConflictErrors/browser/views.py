# -*- coding: UTF-8 -*-
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from . import storage
import datetime
from plone.protect import CheckAuthenticator
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.TrackConflictErrors.interfaces import IConflictTrackerSchema
from .TrackerThread import TrackerThread

class TrackerView(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request        

    def getTrackerResults(self):
        result=storage.get_Results(self.context) 
        if result==dict():
           self.results={}
        else:
            self.results=result['count'][::-1]
        return self.results

    def getLastReset(self):
        result=storage.get_Results(self.context)
        if result==dict():
           return datetime.datetime.now()
        else:
           return result['reset'] 

class ClearTracker(BrowserView):
    def __call__(self):
        CheckAuthenticator(self.context.REQUEST)
        storage.clear(self.context)
        IStatusMessage(self.context.REQUEST).addStatusMessage(("Logging history cleared successfully"), type="info")

class StartTracker(BrowserView):
    def __call__(self):
        CheckAuthenticator(self.context.REQUEST)
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IConflictTrackerSchema)
        path=settings.Log_Root_Path
        clients=settings.Number_Clients
        files=[]
        try:
            if clients==1:
                files.append(open((path+'/instance/event.log')))
            else:
                for item in range(1,clients+1):
                    files.append(open((path+'/client'+str(item)+'/event.log')))
        except Exception:
            raise
        trackerThread=TrackerThread(files)
        try:
            trackerThread.start() 
            IStatusMessage(self.context.REQUEST).addStatusMessage(("Tracker Start successfully"), type="info")
        except Exception:
            import sys
            print sys.exec_info()
