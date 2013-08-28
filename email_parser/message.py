import re

from email.utils import parsedate_tz

__all__ = [
    'Person',
    'EmailMessage',
]


class Person(object):
    def __init__(self, email, name=None):
        self.email = email
        self.name = name

    @classmethod
    def from_string(klass, string):
        match = re.match('(.*?)\s?<(.*?)>', string)

        if not match:
            return None

        name = match.group(1) or None
        email = match.group(2)

        return klass(name=name, email=email)

    def __str__(self):
        return ('<Person email=%s, name=%s>' % (self.email, self.name))


class EmailMessage(object):
    def __init__(self, uid, headers, text_body=None, html_body=None,
                 read=False):
        self.uid = uid
        self.subject = headers.get('Subject', None)
        self.date = headers.get('Date', None)
        self.text_body = text_body
        self.html_body = html_body
        self.read = read

        if headers.get('From', None):
            self.sender = Person.from_string(headers['From'])
        else:
            self.sender = None

        if headers.get('Date', None):
            self.date = parsedate_tz(headers['Date'])
        else:
            self.date = None

        self.headers = headers

    def get_unsubscribe_link(self):
        list_unsubscribe = self.headers.get('List-Unsubscribe', None)

        if not list_unsubscribe:
            return None

        values = list_unsubscribe.strip().replace('<', '').replace('>', '').split(',')

        for value in values:
            if value.startswith('http://') or value.startswith('https://'):
                url = value.replace('<', '').replace('>', '').strip()
                return url

        return None

    def __str__(self):
        if self.sender:
            sender = self.sender.email
        else:
            sender = None

        return ('<Message uid=%s, subject="%s", sender=%s>' %
                (self.uid, self.subject, sender))
