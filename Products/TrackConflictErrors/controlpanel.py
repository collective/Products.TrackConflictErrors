# -*- coding: UTF-8 -*-
from plone.app.registry.browser import controlpanel
from Products.TrackConflictErrors import _
from Products.TrackConflictErrors.interfaces import IConflictTrackerSchema

class ConflictTrackerSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IConflictTrackerSchema
    label = _(u"ConflictTrackerSettings")
    description = _(u"This form enable the user to change the configuration parameters of ConflictTracker Product")

    def updateFields(self):
        super(ConflictTrackerSettingsEditForm, self).updateFields()


    def updateWidgets(self):
        super(ConflictTrackerSettingsEditForm, self).updateWidgets()

class ConflictTrackerSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ConflictTrackerSettingsEditForm


