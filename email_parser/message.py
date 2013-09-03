import re

from email.utils import parsedate_tz

__all__ = [
    'Person',
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
        match = re.match('(.*?)\s?<(.*?)>', string)

        if not match:
            return None

        name = match.group(1) or None
        email = match.group(2)

        return klass(name=name, email=email)

    def __str__(self):
        return ('<Person email=%s, name=%s>' % (self.email, self.name))


class Message(object):
    uid = None
    subject = None
    sender = None
    receiver = None

    text_body = None
    html_body = None

    # Misc metadata and fields
    read = None
    message_id = None
    in_reply_to = None

    headers = {}

    def __init__(self, uid, subject, sender, receiver, headers, read=None,
                 text_body=None, html_body=None):
        self.uid = uid
        self.subject = subject
        self.sender = sender
        self.receiver = receiver
        self.headers = headers
        self.read = read

        self.text_body = text_body
        self.html_body = html_body

        if headers.get('Date', None):
            self.date = parsedate_tz(headers['Date'])
        else:
            self.date = None

        self.headers = headers

    def __str__(self):
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
