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
            self.results=result['count']
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
    count=0
    tObject=None
    def __call__(self):
        if getattr(self.context.REQUEST, 'closebutton', None) is not None:
            if StartTracker.tObject is not None:
                StartTracker.tObject.pause()
                IStatusMessage(self.context.REQUEST).addStatusMessage(("Logging Process Stopped"), type="info")
            else:
                IStatusMessage(self.context.REQUEST).addStatusMessage(("Please Start the Logging first"), type="error")
        elif getattr(self.context.REQUEST, 'startbutton', None) is not None:
            StartTracker.count+=1
            CheckAuthenticator(self.context.REQUEST)
            try:
                self.processFiles()
            except Exception:
                import sys
                print sys.exc_info()
        elif getattr(self.context.REQUEST, 'refreshbutton', None) is not None:
             if StartTracker.tObject is not None:
                 StartTracker.tObject.processLines(self.context)
                 IStatusMessage(self.context.REQUEST).addStatusMessage(("Entries Refreshed Successfully"), type="info")
             else:
                IStatusMessage(self.context.REQUEST).addStatusMessage(("Please Start the Logging first"), type="error")

    def processFiles(self):
        if StartTracker.count==1:
           registry = getUtility(IRegistry)
           settings = registry.forInterface(IConflictTrackerSchema)
           path=settings.Log_Root_Path
           clients=settings.Number_Clients
           files=[]
           try:
                if clients==1:
                    files.append(open((path+'/instance/event.log'),'r'))
                else:
                    for item in range(1,clients+1):
                        files.append(open((path+'/client'+str(item)+'/event.log'),'r'))
           except Exception:
                raise
           """files=open((path+'/client1/event.log'),'rt')"""
           StartTracker.tObject=TrackerThread(self.context,files)
           try:
                StartTracker.tObject.start() 
                IStatusMessage(self.context.REQUEST).addStatusMessage(("Tracker Start successfully"), type="info")
           except Exception:
                import sys
                print sys.exc_info()
                raise
        elif StartTracker.count>1:
            StartTracker.tObject.resume()         
            IStatusMessage(self.context.REQUEST).addStatusMessage(("Logging resumed successfully"), type="error")
