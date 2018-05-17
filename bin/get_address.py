#!/usr/bin/env python
# coding=utf-8
#
# Copyright © 2011-2015 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import absolute_import, division, print_function, unicode_literals

from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators
import sys


@Configuration()
class GetAddressCommand(StreamingCommand):
    """ Counts the number of non-overlapping matches to a regular expression in a set of fields.

    ##Syntax

    .. code-block::
        get_address field=<field-to-convert>

    ##Description

    Using python, converts raw string decimal into legitimate hex fields without letter representation.

    ##Example

    Convert, using python, raw strings for decimals representations into their hexadecimal values.

    .. code-block::
        | <base search> | get_address field=<field-to-convert>

    """
    field = Option(
        doc='''
        **Syntax:** **fieldname=***<fieldname>*
        **Description:** Name of the field that will hold the match count''',
        require=True, validate=validators.Fieldname())

    def stream(self, records):
        self.logger.debug('CountMatchesCommand: %s', self)  # logs command line
        for record in records:
            record[str(self.field+"_raw")] = str(hex(int(record[self.field])))
            yield record

dispatch(GetAddressCommand, sys.argv, sys.stdin, sys.stdout, __name__)
