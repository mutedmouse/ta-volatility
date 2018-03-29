from __future__ import absolute_import, division, print_function, unicode_literals

from splunklib.searchcommands import dispatch, ReportingCommand, Configuration, Option, validators
import sys
import collections

@Configuration(requires_preop=False)
class ListProcessCommand(ReportingCommand):
    """ List all child processes of the field.
    """
    root_process_id = Option(
        doc='''
        **Syntax:** **root_process_id=***<fieldname>*
        **Description:** Root process id''',
        require=True, validate=validators.Integer(0))

    process_field = Option(
        doc='''
        **Syntax:** **process_field=***<fieldname>*
        **Description:** Name of the process field''',
        require=True, validate=validators.Fieldname())

    ppid_field = Option(
        doc='''
        **Syntax:** **ppid_field=***<fieldname>*
        **Description:** Name of the parent process id field''',
        require=True, validate=validators.Fieldname())

    pid_field = Option(
        doc='''
        **Syntax:** **pid_field=***<fieldname>*
        **Description:** Name of the process id field''',
        require=True, validate=validators.Fieldname())

    @Configuration()

    def map(self, records):
        return records

    def reduce(self, records):
        tree = collections.defaultdict(list)
        name_id = collections.defaultdict(list)
        pid_ppid = collections.defaultdict(list)
        q = collections.deque()
        o = collections.deque()
        for record in records:
          tree[record[self.ppid_field]].append(record[self.pid_field])
          name_id[record[self.pid_field]].append(record[self.process_field])
          pid_ppid[record[self.pid_field]].append(record[self.ppid_field])

        q.append(str(self.root_process_id))
        o.append(str(self.root_process_id))
        while len(q) > 0:
            children = tree[q.popleft()]
            for child in children:
                q.append(child)
                o.append(child)

        while len(o)>0:
            pid=o.popleft()
            yield {self.process_field: name_id[pid],self.pid_field:pid,self.ppid_field:pid_ppid[pid]}

dispatch(ListProcessCommand, sys.argv, sys.stdin, sys.stdout, __name__)
