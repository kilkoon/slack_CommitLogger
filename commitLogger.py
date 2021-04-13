from pandas import json_normalize
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
import time
import sys

SLACK_TOKEN = sys.argv[1]
print(SLACK_TOKEN)
USER_ID_GITHUB = 'U01TZS78865'

client = WebClient(token=SLACK_TOKEN)

# 채널 조회
result = client.conversations_list()
channel_list = json_normalize(result['channels'])
channel_id = list(channel_list.loc[channel_list['name'] == '커밋-인증', 'id'])[0]

# 채널 조인
client.conversations_join(token=SLACK_TOKEN, channel=channel_id)

# 채팅 조회
result = client.conversations_history(token=SLACK_TOKEN, channel=channel_id)

conversations_list = result['messages']
conversation_list_github = list(filter(lambda x:x['user']==USER_ID_GITHUB, conversations_list))

for conv in conversation_list_github:
    # print(conv)
    if 'attachments' in conv:
        attachment = conv['attachments'][0]
        if 'author_name' in attachment:
            timestamp = conv['ts'].split('.')[1]
            # print(datetime.utcfromtimestamp(int(timestamp)))
            print(attachment['author_name'] + ":" + attachment['fallback'])

# 포스팅
# client.chat_postMessage(channel=channel_id, text="test clientLogger") 