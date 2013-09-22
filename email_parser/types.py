import re

import pytz
from datetime import datetime
from email.utils import parsedate_tz, mktime_tz

__all__ = [
    'Person',
    'Mailbox',

    'Message',
    'OutgoingMessage',
    'IncomingMessage'
]


class Person(object):
    def __init__(self, email, name=None):
        self.email = email
        self.name = name

    @classmethod
    def from_string(klass, string):
        if not string:
            return None

        match = re.match('(.*?)\s?<(.*?)>', string)

        if match:
            name = match.group(1) or None
            email = match.group(2)
        else:
            # Assume only email is provided
            name = None
            email = string

        return klass(name=name, email=email)

    def __repr__(self):
        return ('<Person email=%s, name=%s>' % (self.email, self.name))


class Mailbox(object):
    name = None
    flags = None

    def __init__(self, name, flags):
        self.name = name
        self.flags = flags

    def __repr__(self):
        return ('<Mailbox name=%s, flags=%s>' % (self.name, self.flags))


class Message(object):
    uid = None
    subject = None
    sender = None
    recipient = None

    text_body = None
    html_body = None

    # Misc metadata and fields
    read = None
    message_id = None
    in_reply_to = None

    headers = {}

    def __init__(self, uid, subject, sender, recipient, headers, read=None,
                 text_body=None, html_body=None):
        self.uid = int(uid) if uid else None
        self.subject = subject
        self.sender = sender
        self.recipient = recipient
        self.headers = headers
        self.read = read

        self.text_body = text_body
        self.html_body = html_body

        if headers.get('Date', None):
            date = mktime_tz(parsedate_tz(headers['Date']))
            date = datetime.fromtimestamp(date, pytz.utc)
            self.date = date
        else:
            self.date = None

        self.headers = headers

    def __repr__(self):
        if self.sender:
            sender = self.sender.email
        else:
            sender = None

        return ('<Message uid=%s, subject="%s", sender=%s>' %
                (self.uid, self.subject, sender))


class IncomingMessage(Message):
    date_sent = None
    date_received = None

    spf_signature = None
    dkim_signature = None

    valid_dkim_signature = None
    valid_spf_signature = None

    def __init__(self, *args, **kwargs):
        self.date_sent = kwargs.pop('date_sent')
        self.date_received = kwargs.pop('date_received')

        self.spf_signature = kwargs.pop('spf_signature')
        self.dkim_signature = kwargs.pop('dkim_signature')

        self.valid_spf_signature = kwargs.pop('valid_spf_signature')
        self.valid_dkim_signature = kwargs.pop('valid_dkim_signature')
        super(IncomingMessage, self).__init__(*args, **kwargs)


class OutgoingMessage(Message):
    date_sent = None

    def __init__(self, *args, **kwargs):
        self.date_sent = kwargs.pop('date_sent')
        super(OutgoingMessage, self).__init__(*args, **kwargs)
