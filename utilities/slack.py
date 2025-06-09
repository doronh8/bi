# ! /usr/bin/env python
#
'''
cd c:\BI\Batch
python Files.py

git checkout -- Batch/Files.py

import AllFunctions

'''

import os


class SlackObject:
    """
    Create Slack Object
    """

    # BEARER = "Bearer xoxb-5974653924898-7032491956727-foklFGmLdag9x9qm1DpdwN1w"
    # CHANNEL = "analytics-alerts"

    def __init__(self, suite_name, channel, bearer):
        """
        init
        """
        self._suite_name = suite_name
        self.CHANNEL = channel
        self.BEARER = bearer
        self._slack_curl = \
            'curl -d "text={}" -d "channel={}" -H "Authorization: {}" -X POST "https://slack.com/api/chat.postMessage"' \
                .format('<ReplaceMessage>', self.CHANNEL, self.BEARER)

    ############ Slack Msg ############
    def update_with_slack_message(self, message):
        """
        Updates With Slack Message
        """
        _curl_cmd = self._slack_curl.replace('<ReplaceMessage>',
                                             message).replace('`', '\`')
        print(_curl_cmd)
        os.system(_curl_cmd)