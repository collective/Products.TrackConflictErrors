# -*- coding: UTF-8 -*-
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from . import storage
import datetime
from plone.protect import CheckAuthenticator
from Products.statusmessages.interfaces import IStatusMessage

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
