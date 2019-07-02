# -*- coding: UTF-8 -*-

# 709758847

from fbchat import log, Client
from fbchat.models import *
import json
import os

from svultron import svultron

# Subclass fbchat.Client and override required methods
class EchoBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        if author_id != self.uid and message_object.text[0] == '!':
            # load commands
            with open('commands.json') as command_config:
                json_commands = command_config.read()
                commands = json.loads(json_commands)

                if message_object.text[1:] == 'svultron':
                    let reply_text = svultron()
                    reply_text = commands[message_object.text[1:]]
                    log.info("{}: reply text: '{}'".format(message_object.text[1:], reply_text))
                    client.send(Message(text=reply_text), thread_id=thread_id, thread_type=thread_type)
                else if message_object.text[1:] in commands:
                    reply_text = commands[message_object.text[1:]]
                    log.info("{}: reply text: '{}'".format(message_object.text[1:], reply_text))
                    client.send(Message(text=reply_text), thread_id=thread_id, thread_type=thread_type)
                else:
                    log.info("Ignoring unknown command {}".format(message_object.text[1:]))


email = os.environ.get('EMAIL')
password = os.environ.get('PASSWD')

if email is None or password is None:
    print "Please set environment variables to be able to login."
    print "\tEMAIL   - The email of the user."
    print "\tPASSWD  - The password of the user."
else:
    client = EchoBot(email, password)
    client.listen()