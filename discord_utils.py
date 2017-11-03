import time
import asyncio
import string

@asyncio.coroutine
def slow_send(client, dest, content=None, delay=1, tts=False, embed=None):
    yield from client.send_typing(dest)
    time.sleep(delay)
    yield from client.send_message(dest, content=content, tts=tts, embed=embed)
               
def _finish_token(tokens, current):
    while len(current) and current[len(current) - 1] in string.punctuation:
        punc = current[-1]
        current = current[:-1]
        tokens, current = _finish_token(tokens, current)
        if len(current):
            tokens.append("".join(current))
            current = list()
        tokens.append(punc)
    tokens.append(current)
    current = ""
    return (tokens, current)
                                                                         
def tokenize(text):
    tokens = list()
    current = ""

    for char in text:
        if char in string.punctuation and char != '@' and len(current) == 0:
            tokens.append(char)
        elif char in string.whitespace:
            tokens, current = _finish_token(tokens, current)
        else:
            current += char.lower()

    tokens, current = _finish_token(tokens, current)

    return tokens
