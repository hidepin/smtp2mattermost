#!/usr/bin/env python

import smtpd
import asyncore

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
        print('Message header  :', header)
        print('---------- body ----------')
        print('Message body  :', body)
        return

server = CustomSMTPServer(('0.0.0.0', 1025), None, decode_data=True)

asyncore.loop()
