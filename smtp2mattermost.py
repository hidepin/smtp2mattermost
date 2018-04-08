#!/usr/bin/env python

import smtpd
import asyncore
import re
import quopri
from email.header import decode_header

class CustomSMTPServer(smtpd.SMTPServer):
    def __init__(self, localaddr, remoteaddr, data_size_limit=33554432, map=None, enable_SMTPUTF8=False, decode_data=False):
        # 再利用している
        super(CustomSMTPServer, self).__init__(localaddr, remoteaddr, data_size_limit, map, enable_SMTPUTF8, decode_data)

    def process_message(self, peer, mailfrom, rcpttos, data):
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to  :', rcpttos)
        print('Message length        :', len(data))
        (header, body) = data.split('\n\n\n')
        print('---------- header ----------')
        for line in header.split('\n'):
            pattern = re.compile("Subject")
            match = pattern.match(line)
            if match != None:
                print('Subject  :', decode_header(line)[1][0].decode('utf-8'))
            else:
                print(line)
        print('---------- body ----------')
        print(quopri.decodestring(body).decode('utf-8'))
        return

server = CustomSMTPServer(('0.0.0.0', 1025), None, decode_data=True)

asyncore.loop()
