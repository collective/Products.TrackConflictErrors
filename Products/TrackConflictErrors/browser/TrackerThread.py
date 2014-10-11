import threading
import time
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.TrackConflictErrors.interfaces import IConflictTrackerSchema
from .storage import add_to_count
import datetime
import ZODB

class TrackerThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,context,files):
        super(TrackerThread, self).__init__()
        self.files=files
        self.context=context
        self.paused = True  # start out paused
        self.state = threading.Condition()
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IConflictTrackerSchema)
        self.time_interval=settings.Time_Interval
        self.results=[]

    def run(self):
        self.resume()
        patteren="conflict error"
        while True:
            with self.state:
                if self.paused:
                    self.state.wait() # block until notified
            for item in self.files:
                for items in item:
                    if patteren in items:
                        self.results.append(items)
                else:
                    item.seek(item.tell())
            time.sleep(self.time_interval)
           
            
    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # unblock self if waiting

    def pause(self):
        with self.state:
            self.paused = True  # make self block and wait
            print "Thread Got Paused"

    def processLines(self,context):
           for result in self.results:
               items=result.split()
               time=items[0]
               items=items[1:]
               action=' '.join(items)
               add_to_count(context,time,action)
           

