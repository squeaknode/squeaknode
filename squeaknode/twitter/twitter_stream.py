# MIT License
#
# Copyright (c) 2020 Jonathan Zernik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import json
import os
from typing import Iterable
from typing import List

import requests


# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


class TwitterStream:

    TWITTER_STREAM_URL = "https://api.twitter.com/2/tweets/search/stream"
    TWITTER_STREAM_RULES_URL = "https://api.twitter.com/2/tweets/search/stream/rules"

    def __init__(self, bearer_token: str, handles: List[str]):
        self.bearer_token = bearer_token
        self.handles = handles

    def get_tweets(self) -> Iterable[dict]:
        rules = self.get_rules()
        delete = self.delete_all_rules(rules)
        set = self.set_rules(delete)
        yield from self.get_stream(set)

    @property
    def bearer_oauth_fn(self):
        def bearer_oauth(r):
            """
            Method required by bearer token authentication.
            """

            r.headers["Authorization"] = f"Bearer {self.bearer_token}"
            r.headers["User-Agent"] = "v2FilteredStreamPython"
            return r
        return bearer_oauth

    def get_rules(self):
        response = requests.get(
            self.TWITTER_STREAM_RULES_URL,
            auth=self.bearer_oauth_fn
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot get rules (HTTP {}): {}".format(
                    response.status_code, response.text)
            )
        print(json.dumps(response.json()))
        return response.json()

    def delete_all_rules(self, rules):
        if rules is None or "data" not in rules:
            return None

        ids = list(map(lambda rule: rule["id"], rules["data"]))
        payload = {"delete": {"ids": ids}}
        response = requests.post(
            self.TWITTER_STREAM_RULES_URL,
            auth=self.bearer_oauth_fn,
            json=payload
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot delete rules (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        print(json.dumps(response.json()))

    def set_rules(self, delete):
        from_strs = [f"from:{handle}" for handle in self.handles]
        rule_value = ' OR '.join(from_strs)
        sample_rules = [
            {"value": rule_value},
        ]
        payload = {"add": sample_rules}
        response = requests.post(
            self.TWITTER_STREAM_RULES_URL,
            auth=self.bearer_oauth_fn,
            json=payload,
        )
        if response.status_code != 201:
            raise Exception(
                "Cannot add rules (HTTP {}): {}".format(
                    response.status_code, response.text)
            )
        print(json.dumps(response.json()))

    def get_stream(self, set) -> Iterable[dict]:
        response = requests.get(
            self.TWITTER_STREAM_URL,
            auth=self.bearer_oauth_fn,
            stream=True,
        )
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Cannot get stream (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        for response_line in response.iter_lines():
            if response_line:
                json_response = json.loads(response_line)
                yield json_response


def print_tweets(tweet_stream):
    for tweet in tweet_stream:
        print(json.dumps(tweet, indent=4, sort_keys=True))


def main():
    twitter_sub = TwitterStream(
        bearer_token=bearer_token,
        handles=['rterqwerqeqwe', 'fooooooo']
    )
    tweet_stream = twitter_sub.get_tweets()
    print_tweets(tweet_stream)


if __name__ == "__main__":
    main()
