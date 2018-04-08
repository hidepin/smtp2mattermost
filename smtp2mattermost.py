#!/usr/bin/env python

import smtpd
import asyncore

class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, mail_options, rcpt_options):
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to  :', rcpttos)
        print('Message length        :', len(data))
        print('Message data  :', data)
        print('Message mail_options  :', mail_options)
        print('Message rcpt_options  :', rcpt_options)
        return

server = CustomSMTPServer(('192.168.0.9', 1025), None)

asyncore.loop()
