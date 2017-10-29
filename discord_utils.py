import time
import asyncio

@asyncio.coroutine
def slow_send(client, dest, content=None, delay=1, tts=False, embed=None):
    yield from client.send_typing(dest)
    time.sleep(delay)
    yield from client.send_message(dest, content=content, tts=tts, embed=embed)
               
