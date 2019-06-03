from xml.etree import ElementTree
from datetime import datetime
import json


dataset_files = {
    "CR": {
        "dev": "./InterTASS/CR/intertass-CR-development-tagged.xml",
        "test": "./InterTASS/CR/intertass-CR-test.xml",
        "train": "./InterTASS/CR/intertass-CR-train-tagged.xml"
    },

    "ES": {
        "dev": "./InterTASS/ES/intertass-ES-development-tagged.xml",
        "test": "./InterTASS/ES/intertass-ES-test.xml",
        "train": "./InterTASS/ES/intertass-ES-train-tagged.xml"
    },

    "PE": {
        "dev": "./InterTASS/PE/intertass-PE-development-tagged.xml",
        "test": "./InterTASS/PE/intertass-PE-test.xml",
        "train": "./InterTASS/PE/intertass-PE-train-tagged.xml"
    }
}


class AspectTASSReader:

    def __init__(self, filename, res_filename=None):
        self.filename = filename
        self.res_filename = res_filename

        self.root = ElementTree.parse(filename).getroot()

    def tweets(self):
        """Iterator over the tweets."""
        for tweet_el in self.root:
            tweet = {}

            tweet['content'] = ''.join(tweet_el.itertext())

            sentiments = []
            for sent_el in tweet_el:
                attrib = sent_el.attrib
                # assert set(attrib) == {'aspect', 'polarity'}
                # one exception: <sentiment>#HalaMadrid</sentiment>
                sent = dict(attrib)
                sent['text'] = sent_el.text
                sentiments.append(sent)

            tweet['sentiments'] = sentiments

            yield tweet

    def X(self):
        """Iterator over the aspects and their context."""
        for tweet_el in self.root:
            content = ''.join(tweet_el.itertext())

            for sent_el in tweet_el:
                attrib = sent_el.attrib
                sent = dict(attrib)
                sent['text'] = sent_el.text

                if 'aspect' in sent:
                    yield {
                        'context': content,
                        'aspect': sent['aspect'],
                        'text': sent['text']
                    }

    def y(self):
        """Iterator over the aspect polarities."""
        for tweet_el in self.root:
            for sent_el in tweet_el:
                attrib = sent_el.attrib
                sent = dict(attrib)
                sent['text'] = sent_el.text

                if 'aspect' in sent:
                    yield sent['polarity']


class GeneralTASSReader:

    def __init__(self, filename, res_filename=None, simple=False):
        self.filename = filename
        self.res_filename = res_filename
        self.simple = simple

        self.root = ElementTree.parse(filename).getroot()
        self.smapdict = smapdict = {}
        if simple:
            smapdict['P+'] = 'P'
            smapdict['N+'] = 'N'

    def tweets(self):
        """Iterator over the tweets."""

        def smap(sentiment):
            return self.smapdict.get(sentiment, sentiment)

        for tweet_el in self.root:
            # assert len(tweet_el) in [5, 7]
            attrs = ['tweetid', 'user', 'content', 'date', 'lang']
            tweet = {}
            for attr in attrs:
                tweet[attr] = tweet_el.find(attr).text

            # parse date
            tweet['date'] = datetime.strptime(tweet['date'], '%Y-%m-%dT%H:%M:%S')

            sentiments_el = tweet_el.find('sentiments')
            if sentiments_el:
                # general sentiment
                polarity_el = sentiments_el[0]
                tweet['sentiment'] = {
                    'value': smap(polarity_el.find('value').text),
                    'type': polarity_el.find('type').text
                }

                # entity sentiments
                tweet['sentiments'] = []
                for polarity_el in sentiments_el[1:]:
                    polarity = {
                        'entity': polarity_el.find('entity').text,
                        'value': smap(polarity_el.find('value').text),
                        'type': polarity_el.find('type').text
                    }
                    tweet['sentiments'].append(polarity)

                # now the topics
                tweet['topics'] = []
                for topic_el in tweet_el.find('topics'):
                    tweet['topics'].append(topic_el.text)

            yield tweet

    def X(self):
        """Iterator over the tweet contents."""

        for tweet_el in self.root:
            # assert len(tweet_el) in [5, 7]
            content = tweet_el.find('content').text or ''
            yield content

    def y(self):
        """Iterator over the tweet polarities."""
        def smap(sentiment):
            return self.smapdict.get(sentiment, sentiment)

        if self.res_filename is None:
            # development dataset
            for tweet_el in self.root:
                assert len(tweet_el) == 7
                # general sentiment
                polarity_el = tweet_el.find('sentiments')[0]
                sentiment = smap(polarity_el.find('value').text)
                yield sentiment
        else:
            # test dataset.
            # tweets in the qrel file must be in the same order as in the XML
            with open(self.res_filename, 'r') as f:
                for line in f:
                    sentiment = line.split()[-1]
                    yield sentiment


class InterTASSReader:

    def __init__(self, filename, res_filename=None):
        self.filename = filename
        self.res_filename = res_filename
        self.root = ElementTree.parse(filename).getroot()

    def tweets(self):
        """Iterator over the tweets."""
        for tweet_el in self.root:
            assert len(tweet_el) == 6
            attrs = ['tweetid', 'user', 'content', 'date', 'lang']
            tweet = {}
            for attr in attrs:
                tweet[attr] = tweet_el.find(attr).text
            # now the sentiment
            tweet['sentiment'] = tweet_el.find('sentiment')[0][0].text

            # parse date
            try:
                tweet['date'] = datetime.strptime(tweet['date'], '%Y-%m-%d %H:%M:%S')
            except:
                tweet['date'] = datetime.strptime(tweet['date'], '%a %b %d %H:%M:%S %z %Y')

            yield tweet

    def X(self):
        """Iterator over the tweet contents."""
        for tweet_el in self.root:
            assert len(tweet_el) == 6
            content = tweet_el.find('content').text
            yield content

    def y(self):
        """Iterator over the tweet polarities."""
        if self.res_filename is None:
            # development dataset
            for tweet_el in self.root:
                assert len(tweet_el) == 6
                sentiment = tweet_el.find('sentiment')[0][0].text
                yield sentiment
        else:
            # test dataset
            with open(self.res_filename, 'r') as f:
                for line in f:
                    sentiment = line.split()[-1]
                    yield sentiment

    def tweetIds(self):
        """Iterator over the tweetIds."""

        for tweet_el in self.root:
            content = tweet_el.find('tweetid').text or ''
            yield content


class JSONReader:
    """ This is used for synthetic tweets generated by user. """
    def __init__(self, filename):
        self.filename = filename
        self.contents = None

    def _preload_contents(self):
        if self.contents is None:
            self.contents = json.load(open(self.filename))

    def tweets(self):
        self._preload_contents()

        return self.contents

    def X(self):
        self._preload_contents()
        for instance in self.contents:
            yield instance["text"]

    def y(self):
        self._preload_contents()
        for instance in self.contents:
            yield instance["label"]

    def tweetIds(self):
        self._preload_contents()
        for instance in self.contents:
            yield instance["tweetid"]

