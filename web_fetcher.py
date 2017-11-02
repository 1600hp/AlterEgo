import pycurl
import re
from io import BytesIO
import editdistance
import discord 
import asyncio
import json
from urllib import parse

from interpretation import Interpretation
from discord_utils import slow_send

class MTGFetcher(Interpretation):
    def __init__(self, client):
        self.cached_target = None
        self.cached = None
        self.client = client

    def query(self, target):
        if target == self.cached_target:
            body = self.cached
        else:
            buffer = BytesIO()
            c = pycurl.Curl()
            c.setopt(c.URL, 'https://api.deckbrew.com/mtg/cards?name={}'.format(parse.quote(target)))
            c.setopt(c.WRITEDATA, buffer)
            c.perform()
            c.close()
            body = buffer.getvalue().decode('iso-8859-1')
        self.cached_target = target
        self.cached = body
        return body

    @asyncio.coroutine
    def rate(self, msg, target=None, **kwargs):
        if target == None: return 0
        body = query(target)
        return 0 if (not body or len(body) == 0) else 1

    @asyncio.coroutine
    def apply(self, msg, target=None, **kwargs):
        if target == None: return 0

        body = self.query(target)

        if not body or len(body) == 0: return
        body = json.loads(body)
        if len(body) == 0: return
        distances = [editdistance.eval(target, card["name"]) for card in body]
        best = distances.index(min(distances))
        card = body[best]

        typeline = " ".join([t.title() for t in card["types"]])
        if "subtypes" in card.items():
             typeline += " - " + " ".join([t.title() for t in card["subtypes"]])
        mana = card["cost"]
        text = card["text"]
        description = "{}\n{}\n{}".format(typeline, mana, text)
        try:
            color = card["colors"]
            if len(color) > 1:
                color = 0xefc321
            elif color[0] == "black":
                color = 0x111111
            elif color[0] == "white":
                color = 0xEEEEEE
            elif color[0] == "green":
                color = 0x009900
            elif color[0] == "blue":
                color = 0x0066ff
            elif color[0] == "red":
                color = 0x990000
        except:
            color = 0x555555

        embed = discord.Embed(description=description, color=color)
        embed.set_author(name=card["name"], url=card["editions"][0]["store_url"])
        for ed in card["editions"]:
            if not ed["multiverse_id"] == 0:
                embed.set_image(url=ed["image_url"])
                break

        yield from slow_send(self.client, msg.channel, embed=embed)


class WebFetcher(Interpretation):
    def __init__(self, client):
        self.client = client
        self.bracket_pattern = re.compile("\[\[[^\[\]]+\]\]")
        self.fetchers = [MTGFetcher(client)]
        pass

    @asyncio.coroutine
    def rate(self, msg, **kwargs):
        if re.search(self.bracket_pattern, msg.content):
            return 1
        else:
            return 0

    @asyncio.coroutine
    def apply(self, msg, **kwargs):
        for match in re.findall(self.bracket_pattern, msg.content):
            target = match[2:-2]
            rates = []
            for fetcher in self.fetchers:
                rate = yield from fetcher.rate(msg)
                rates.append(rate)
            fetcher = self.fetchers[rates.index(max(rates))]
            yield from fetcher.apply(msg, target=target)

