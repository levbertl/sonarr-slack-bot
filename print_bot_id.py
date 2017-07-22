import os
import ConfigParser
from slackclient import SlackClient

config = ConfigParser.ConfigParser()
config.readfp(open(r'config.txt'))

BOT_NAME = 'tvbot'
SLACK_BOT_TOKEN = config.get('Slack Config', 'SLACK_BOT_TOKEN')
slack_client = SlackClient(SLACK_BOT_TOKEN)

if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME)