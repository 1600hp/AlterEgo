import pycurl
import re
from io import BytesIO

from interpretation import Interpretation

class MTGFetcher(Interpretation):
    def __init__(self):
        pass

    def rate(self, msg):
        return 1

    def apply(self, msg):
        print(msg)
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, 'https://api.deckbrew.com/mtg/cards?name={}'.format(msg))
        c.setopt(c.WRITEDATA, buffer)
        c.perform
        c.close()

        body = buffer.getvalue().decode('iso-8859-1')
        print(body)

class WebFetcher(Interpretation):
    def __init__(self):
        self.bracket_pattern = re.compile("\[[^\[\]]+\]")
        self.fetchers = [MTGFetcher()]
        pass

    def rate(self, msg):
        if re.search(self.bracket_pattern, msg.content):
            return 1
        else:
            return 0

    def apply(self, msg):
        for match in re.findall(self.bracket_pattern, msg.content):
            target = match[1:-1]
            rates = [fetcher.rate(target) for fetcher in self.fetchers]
            fetcher = self.fetchers[rates.index(max(rates))]
            fetcher.apply(target)

