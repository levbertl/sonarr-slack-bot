import time
import ConfigParser
from slackclient import SlackClient
from search_new_show import search_show


config = ConfigParser.ConfigParser()
config.readfp(open(r'config.txt'))

# starterbot's ID as an environment variable
# BOT_ID = "U6B4L5KLJ"
BOT_ID = config.get('Slack Config', 'BOT_ID')

# constants
AT_BOT = "<@" + BOT_ID + ">"
SEARCH_SHOW = "search show "


# instantiate Slack & Twilio clients
SLACK_BOT_TOKEN = config.get('Slack Config', 'SLACK_BOT_TOKEN')
slack_client = SlackClient(SLACK_BOT_TOKEN)


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + SEARCH_SHOW + \
               "* command with numbers, delimited by spaces."
    if command.startswith(SEARCH_SHOW):
        response = search_show(command, SEARCH_SHOW)

    slack_client.api_call("chat.postMessage", channel=channel,
                          text="test", attachments=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("TV Bot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")