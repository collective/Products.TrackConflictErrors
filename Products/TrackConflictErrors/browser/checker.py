import os, re
from Products.Five.browser import BrowserView

#
# Assumptions
# -----------
#
# Since St_ctime and Seek are not persisted,
# every time zope is restarted, the log files
# will be reprocessed. No harm since we store only
# increasing timestamps.
#
# We could stick these in another property if needed.
#

Timestamp_Pattern = re.compile('\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}')
St_ctime = {}
Seek = {}

class CheckLog(BrowserView):
    def __call__(self):
        props = self.context.portal_properties.conflicttracker_properties
        conflicts = list(props.timestamps)
        modified = 0
        for file1 in props.logfiles:
            modified += self.process_file(file1, conflicts)
        if modified:
            props.manage_changeProperties(timestamps=conflicts)
        return '%s: %s' % (len(props.logfiles), len(props.timestamps))

    def process_file(self, file1, conflicts):
        stat = os.stat(file1)
        if file1 in St_ctime:
            if St_ctime[file1] != stat.st_ctime:
                St_ctime[file1] = stat.st_ctime
                Seek[file1] = 0
        else:
            St_ctime[file1] = stat.st_ctime
            Seek[file1] = 0

        fp = open(file1)
        fp.seek(Seek[file1])
        modified = False
        last_conflict = conflicts[-1] if conflicts else ''
        while 1:
            line = fp.readline()
            if not line:
                break
            if line.find(' ConflictError ') == -1:
                continue
            timestamp = line.split()[0]
            if Timestamp_Pattern.match(timestamp) and timestamp > last_conflict:
                conflicts.append(timestamp)
                modified = True
        Seek[file1] = fp.tell()
        fp.close()
        return 1 if modified else 0
