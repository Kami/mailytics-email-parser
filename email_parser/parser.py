from imaplib import ParseFlags
from email.parser import Parser

from email_parser.message import EmailMessage


def get_message_text_and_html_part(message):
    payload = message.get_payload()

    if not isinstance(payload, (tuple, list)):
        return None, None

    text_parts = [p for p in payload if p.get_content_type() == 'text/plain']
    html_parts = [p for p in payload if p.get_content_type() == 'text/html']

    text_body, html_body = None, None

    if len(text_parts) >= 1:
        text_body = text_parts[0]

    if len(html_parts) >= 1:
        html_body = html_parts[0]

    return text_body, html_body


def get_message_headers(message):
    headers = {}
    keys = message.keys()

    for key in keys:
        headers[key] = message[key]

    return headers


def parse_imap_message(msg_data):
    parser = Parser()
    uid = msg_data[0][0]
    flags = ParseFlags(msg_data[0])

    read = '\Seen' in flags
    message = parser.parsestr(msg_data[1])
    headers = get_message_headers(message)

    text_body, html_body = get_message_text_and_html_part(message)

    email_message = EmailMessage(uid=uid, headers=headers, text_body=text_body,
                                 html_body=html_body, read=read)
    return email_message


def parse_raw_message(msg_data):
    parser = Parser()
    message = parser.parsestr(msg_data)
    headers = get_message_headers(message)
    text_body, html_body = get_message_text_and_html_part(message)
    uid = None
    read = 'unknown'

    email_message = EmailMessage(uid=uid, headers=headers, text_body=text_body,
                                 html_body=html_body, read=read)
    return email_message


def parse_message(msg_data):
    """
    Parse raw email message and return EmailMessage object.
    """
    if isinstance(msg_data, tuple):
        message = parse_imap_message(msg_data)
    else:
        message = parse_raw_message(msg_data)

    return message
