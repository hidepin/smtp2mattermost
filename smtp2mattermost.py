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
        print('Message data  :', data)
        return

server = CustomSMTPServer(('192.168.0.9', 1025), None, decode_data=True)

asyncore.loop()
