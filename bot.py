# -*- coding: UTF-8 -*-

# 709758847

from fbchat import log, Client
from fbchat.models import *
import json
import os
import random

from svultron import svultron


# Subclass fbchat.Client and override required methods
class EchoBot(Client):
    def send_reply(self, command, reply_text, thread_id, thread_type):
        log.info("{}: reply text: '{}'".format(command, reply_text))
        client.send(
            Message(text=reply_text),
            thread_id=thread_id,
            thread_type=thread_type
        )

    def onMessage(self, uid, msg, tid, ttype, **kwargs):
        self.markAsDelivered(tid, msg.uid)
        self.markAsRead(tid)

        if uid != self.uid and msg.text[0] == '!':
            if msg.text[1:] == 'svultron':
                self.send_reply(msg.text[1:], svultron(), tid, ttype)
            else:
                # load commands
                with open('commands.json') as command_config:
                    json_commands = command_config.read()
                    commands = json.loads(json_commands)

                    if msg.text[1:] in commands:
                        response = commands[msg.text[1:]]
                        if isinstance(response, list):
                            response = random.choice(commands[msg.text[1:]])
                        self.send_reply(
                            msg.text[1:],
                            response,
                            tid,
                            ttype
                        )
                    else:
                        log.info("Unknown '{}'".format(msg.text[1:]))


email = os.environ.get('EMAIL')
password = os.environ.get('PASSWD')

if email is None or password is None:
    print("Please set environment variables to be able to login.")
    print("\tEMAIL   - The email of the user.")
    print("\tPASSWD  - The password of the user.")
else:
    client = EchoBot(email, password)
    client.listen()
