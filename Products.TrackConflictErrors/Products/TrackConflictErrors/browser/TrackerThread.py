import threading
import time
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.TrackConflictErrors.interfaces import IConflictTrackerSchema

class TrackerThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,files):
        print len(files)
        super(TrackerThread, self).__init__()
        self._stop = threading.Event()
        self.files=files
        print self._stop
        print self.files
        
        #registry = getUtility(IRegistry)
        #settings = registry.forInterface(IConflictTrackerSchema)
        #self.time_interval=settings.Time_Interval

    def stop(self):
        self._stop.set()
        for file in self.files:
            file.close()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        print "hi"
        for line in self.files[0]:
            print line,
        """try:
            while not self.stopped():
                for file in self.files:
                    for line in file:
                        print line,
                    else:
                        file.seek(file.tell())
                time.sleep(100);
        except Exception:
            self.stop()
            raise"""

    
