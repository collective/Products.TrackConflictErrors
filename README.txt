Products.TrackConflictErrors
============================

Plone product to keep track of conflict errors. 

It does this by scanning the event log for Conflict Errors.

It exposes a single view method: http://<url-of-plone-site>/track-conflict

Needs to be installed using quickinstaller.

Creates a property sheet under portal_properties/site_properties which contains the timestamps of the conflict errors.
