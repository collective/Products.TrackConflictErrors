from zope.annotation.interfaces import IAnnotations
from persistent.list import PersistentList
from persistent.dict import PersistentDict
from Products.CMFCore.utils import getToolByName
import datetime 
TRACKBY = "Products.TrackConflictErrors.Trackby"
 
 
def setupAnnotations(context):
    """
    set up the annotations if they haven't been set up
    already. The rest of the functions in here assume that
    this has already been set up
    """
    annotations = IAnnotations(context)
    if not TRACKBY in annotations.keys():
        annotations[TRACKBY] = PersistentDict({
                "count": PersistentList(),
                'reset': datetime.datetime.now()
                })
 
    return annotations
 
 
def add_to_count(context, time=None,action=None):
    """
         This Method will add the time on which conflict occur and name of action which creates the conflict
    """
    annotations = setupAnnotations(context)
    if dict(time=time,action=action) not in annotations[TRACKBY]['count']:
        annotations[TRACKBY]['count'].append(dict(time=time,action=action))
 
 
def clear(context):
    """
	This Method will clear the counter
    """
    annotations = IAnnotations(context)
    annotations[TRACKBY]['count']=PersistentList()
    annotations[TRACKBY]['reset']=datetime.datetime.now()

def get_Results(context):
    annotations = IAnnotations(context)
    return annotations.get(TRACKBY, {})
              
 

