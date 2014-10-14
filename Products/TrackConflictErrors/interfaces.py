""" This Interface contain The various Configuration setting related to Products.TrackConflictErrors"""
# -*- coding: UTF-8 -*-
"""The List of Imports"""
from zope.interface import Interface
from zope import schema
from Products.TrackConflictErrors import _
import os


class IConflictTrackerSchema(Interface):
    Number_Clients=schema.Int(
        title=_(u'label_clients', default=u'Number of plone instances'),
        default=1,
        required=True
    )
    Log_Root_Path=schema.TextLine(
        title=_(u'label_logpath', default=u'Specify the parent directory of event log files'),
        default=os.environ.get('event_root_path'),
        required=True
    )
    Time_Interval=schema.Int(
        title=_(u'label_timeinterval', default=u'Specify the time interval in seconds for processing of event logs'),
        default=600,
        required=True
    )
