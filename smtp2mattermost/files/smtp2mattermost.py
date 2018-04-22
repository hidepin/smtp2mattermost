#!/usr/bin/env python

import smtpd
import asyncore
import re
import quopri
import os
import urllib.request
import json
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

    def get_ticket_url(self, message):
        for line in message.split('\n'):
            if re.match("http://", line):
                return line

    def get_project_name(self, message):
        project_header = os.environ['MATTERMOST_PRIVATE_PROJECT_HEADER']
        for line in message.split('\n'):
            if re.match(project_header, line):
                return re.sub("^" + project_header + " *", '', line)
        return ""

    def send_mattermost(self, mention, message):
        if self.get_project_name(message) != os.environ['MATTERMOST_PRIVATE_PROJECT']:
            public_income_url = os.environ['MATTERMOST_INCOME_URL']
            if public_income_url != "":
                self.send_message(public_income_url, mention, message)

        private_income_url = os.environ['MATTERMOST_PRIVATE_INCOME_URL']
        if private_income_url != "":
            self.send_message(private_income_url, mention, message)

    def send_message(self, url, mention, message):
        method = "POST"
        headers = {"Content-Type" : "application/json"}

        if mention == None:
            mention = "channel"

        data = {"username": os.environ['MATTERMOST_USERNAME'], "text": "@" + mention + "\n" + self.get_ticket_url(message) + "\n" + "```" + message[:int(os.environ['MATTERMOST_MESSAGE_MAX'])] + "\n```"}
        json_data = json.dumps(data, ensure_ascii=False).encode("utf-8")
        request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode("utf-8")

    def process_message(self, peer, mailfrom, rcpttos, data):
        data = bytes(data, encoding='utf-8').decode('iso-2022-jp')
        (header, body) = data.split('\n\n', 1)
        email = self.search_to_address(header)
        if  email != os.environ['MATTERMOST_EXCLUDE_NOTIFICATE']:
            self.send_mattermost(self.username(email), body)
        return

server = Smtp2MattermostServer(('0.0.0.0', 8025), None, decode_data=True)

asyncore.loop()
