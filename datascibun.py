"""
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging
import os.path
import re

import markovify
import numpy as np

from pybot import PyBot

class ResearchText(markovify.NewlineText):
    def word_split(self, sentence):
        return list(sentence)

    def word_join(self, words):
        return ''.join(word for word in words)

class DSBBot(PyBot):

    def bot_init(self):
        """
        Custom initialization. Specify any configuration options you want to
        override, as in particular your OAuth credentials.
        """

        #############################
        #                           #
        # Twitter OAuth Credentials #
        #                           #
        #      FILL THESE IN!       #
        #                           #
        #############################

        # App: Cuteness Overwhelming

        self.config['api_key'] = 'your api key here'
        self.config['api_secret'] = 'your api secret here'
        self.config['access_key'] = 'your access key here'
        self.config['access_secret'] = 'your access secret here'

        #############################
        #                           #
        #   Other config options    #
        #                           #
        # Fill these in if you want #
        #   or otherwise need to.   #
        #                           #
        #############################

        # Custom variables.
        self.config['bot_name'] = 'datascibun'

        # Posts a tweet roughly every hour...give or take 5 minutes. Ish.
        self.config['normal_mean'] = 60
        self.config['normal_std'] = 5
        self.config['tweet_interval'] = lambda: 60 * np.random.normal(
            loc = self.config['normal_mean'], scale = self.config['normal_std'])

        # What shall we do today, skipper?

        # Various possible posting events.
        self.config['post_events'] = ['research', 'shitpost', 'bun']
        self.config['post_events_weights'] = [0.5, 0.35, 0.15]

        # Datasets.
        self.config['research_data_path'] = os.path.join(self.config['bot_name'], 'all_papers.txt')
        self.config['tweet_data_path'] = os.path.join(self.config['bot_name'], 'all_tweets.txt')

        # Markov chain setup. They're different.
        self.config['research_markov_order'] = 5  # by LETTER
        self.config['shitpost_markov_order'] = 3  # by WORD

        # Some other stuff.
        self.config['bun_events_singular'] = ['*flop*', '*stare*', 'periscope']
        self.config['bun_events_multiple'] = ['sniff', 'BINKY', 'crunch', 'dig']
        self.config['bun_events_repeats'] = 10

        # Load in the datasets.

        with open(self.config['research_data_path'], "r") as f:
            try:
                self.config['research_data'] = f.read()
            except IOError:
                logging.error("Unable to read file \"{}\"!".format(self.config['research_data_path']))
                return
        with open(self.config['tweet_data_path'], "r") as f:
            try:
                self.config['tweet_data'] = f.read()
            except IOError:
                logging.error("Unable to read file \"{}\"!".format(self.config['tweet_data_path']))
                return

    def on_tweet(self):
        # Decide what kind of tweet we're making!
        post_type = np.random.choice(self.config['post_events'], p = self.config['post_events_weights'])
        if post_type == 'research':
            status = self._research()
        elif post_type == 'shitpost':
            status = self._shitpost()
        else: # bun!
            status = self._bun()

        # Post the tweet!
        logging.info("Status: {}".format(status))
        self.update_status(status)

    def _research(self):
        markov = ResearchText(self.config['research_data'], state_size = self.config['research_markov_order'])
        title = " ".join(t.capitalize() for t in markov.make_short_sentence(280).split())
        comment = self._shitpost(room = 280 - len(title) - 2)
        return f"{title}: {comment}".strip()

    def _shitpost(self, room = 280):
        markov = markovify.NewlineText(self.config['tweet_data'], state_size = self.config['shitpost_markov_order'])
        return markov.make_short_sentence(room)
    
    def _bun(self):
        logging.info("Posting a bun activity.")
        event_singular = np.random.choice(self.config['bun_events_singular'])
        event_multiple = np.random.choice(self.config['bun_events_multiple'])
        p_singular = np.random.randint(0, self.config['bun_events_repeats'])
        n_multiple = np.random.randint(1, self.config['bun_events_repeats'] + 1)

        # Build the post.
        post = []
        for i in range(n_multiple):
            if i == p_singular:
                post.append(f' {event_singular} ')
            post.append(event_multiple)
        if p_singular >= n_multiple:
            post.append(f' {event_singular}')
        return "".join(post).strip()

    def on_mention(self, tweet, prefix):
        pass

    def on_timeline(self, tweet, prefix):
        pass

    def on_search(self, tweet):
        pass

    def on_follow(self, friend):
        pass

if __name__ == "__main__":
    bot = DSBBot()
    bot.run()
