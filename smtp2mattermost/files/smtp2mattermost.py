#!/usr/bin/env python

import smtpd
import asyncore
import re
import quopri
import os
from email.header import decode_header
from mattermostdriver import Driver

class Smtp2MattermostServer(smtpd.SMTPServer):
    def __init__(self, localaddr, remoteaddr, data_size_limit=33554432, map=None, enable_SMTPUTF8=False, decode_data=False):
        # 再利用している
        super(Smtp2MattermostServer, self).__init__(localaddr, remoteaddr, data_size_limit, map, enable_SMTPUTF8, decode_data)

    def mattermost_login(self):
        mm = Driver({
            'url': os.environ['MATTERMOST_ADDRESS'],
            'login_id': os.environ['MATTERMOST_LOGIN_ID'],
            'password': os.environ['MATTERMOST_PASSWORD'],
            'scheme': 'http',
            'port': int(os.environ['MATTERMOST_PORT']),
            'basepath': '/api/v3',
            'timeout': 30,
        })
        mm.login()
        return mm

    def mattermost_logout(self, mattermost):
        mattermost.logout()

    def search_user(self, mm, email, teams):
        for team_id in teams.keys():
            # driver が対応していないため暫定方法
            members = mm.teams.get_team(team_id='members/' + team_id)
            for member in members:
                # driver が対応していないため暫定方法
                member_info = mm.users.get_user(user_id=member['user_id'] + '/get')
                if member_info['email'] == email:
                    return member_info['username']

    def username(self, email):
        mm = self.mattermost_login()
        teams = mm.teams.get_team(team_id='all')
        username = self.search_user(mm, email, teams)
        self.mattermost_logout(mm)
        return username

    def search_to_address(self, header):
        for line in header.split('\n'):
            if re.match("^To:", line):
                return line.split(' ',1)[1]

    def process_message(self, peer, mailfrom, rcpttos, data):
        (header, body) = data.split('\n\n', 1)
        email = self.search_to_address(header)
        if  email != os.environ['MATTERMOST_EXCLUDE_NOTIFICATE']:
            print(self.username(email))
        return

server = Smtp2MattermostServer(('0.0.0.0', 8025), None, decode_data=True)

asyncore.loop()
