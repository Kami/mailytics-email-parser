import os
import sys
import unittest

from os.path import join as pjoin
from email.utils import parsedate_tz

from email_parser.message import Person
from email_parser.parser import parse_raw_message

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
FIXTURES_DIR = pjoin(CURRENT_DIR, 'fixtures/')
RAW_FIXTURES_DIR = pjoin(FIXTURES_DIR, 'raw/')


class EmailParserTestCase(unittest.TestCase):
    def test_person_from_string(self):
        values = (
            ('Tomaz Muraus <tomaz@tomaz.me>',
             ('Tomaz Muraus', 'tomaz@tomaz.me')),
            ('Tomaz <tomaz@tomaz.me>', ('Tomaz', 'tomaz@tomaz.me')),
            ('<tomaz@tomaz.me>', (None, 'tomaz@tomaz.me'))
        )

        for string, expected in values:
            person = Person.from_string(string)

            self.assertEqual(person.email, expected[1])
            self.assertEqual(person.name, expected[0])

    def test_parse_incoming_raw_message_simple(self):
        msg_data = self._get_fixture(name='addthis_weekly_analytics.txt')
        message = parse_raw_message('incoming', msg_data)

        self.assertEqual(message.subject, 'Your Weekly AddThis Analytics')
        self.assertEqual(message.sender.email, 'support@addthis.com')
        self.assertEqual(message.sender.name, 'AddThis Team')
        self.assertEqual(message.receiver.email, 'tomaz+coachspree@tomaz.me')

        self.assertEqual(message.date_sent,
                         parsedate_tz('Sun, 18 Aug 2013 18:41:25 +0000'))
        self.assertEqual(message.date_received,
                         parsedate_tz('Sun, 18 Aug 2013 11:41:26 -0700 (PDT)'))

        self.assertEqual(message.read, None)
        self.assertTrue(message.valid_spf_signature)
        self.assertTrue(message.valid_dkim_signature)

    def _get_fixture(self, name):
        fixture_path = pjoin(RAW_FIXTURES_DIR, name)

        with open(fixture_path, 'r') as fp:
            content = fp.read().strip()

        return content


if __name__ == '__main__':
    sys.exit(unittest.main())
