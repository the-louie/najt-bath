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
    def send_reply(self, author_id, command, reply_text,
                   thread_id, thread_type):
        author = client.fetchUserInfo(author_id).get(author_id, "<Unknown>")
        log.warning("{}: '{}' -> '{}'".format(
            author.name,
            command,
            reply_text.replace("\n", " | ")
        ))
        client.send(
            Message(text=reply_text),
            thread_id=thread_id,
            thread_type=thread_type
        )

    def onMessage(self, author_id, message_object,
                  thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        if author_id != self.uid and message_object.text[0] == '!':
            # Handle !svultron as a special case. It calls an external
            # module that generates a fake quote based on keywords.
            if message_object.text[1:] == 'svultron':
                self.send_reply(author_id, message_object.text[1:],
                                svultron(), thread_id, thread_type)
            else:
                # re-load commands
                # FIXME: should be a way not needing to reload the
                #        commands.json file every time. maybe add a
                #        command-command like !refresh
                with open('commands.json') as command_config:
                    json_commands = command_config.read()
                    commands = json.loads(json_commands)

                    # If the command exists return the value matching
                    # the key. If the value is a list we return a random
                    # item in that list.
                    if message_object.text[1:] in commands:
                        response = commands[message_object.text[1:]]
                        if isinstance(response, list):
                            response = random.choice(
                                commands[message_object.text[1:]])
                        self.send_reply(
                            author_id,
                            message_object.text[1:],
                            response,
                            thread_id,
                            thread_type
                        )
                    else:
                        log.info("Unknown '{}'".format(
                            message_object.text[1:]))


email = os.environ.get('EMAIL')
password = os.environ.get('PASSWD')

if email is None or password is None:
    print("Please set environment variables to be able to login.")
    print("\tEMAIL   - The email of the user.")
    print("\tPASSWD  - The password of the user.")
else:
    client = EchoBot(email, password, logging_level=30)
    client.listen()
