import asyncio

# Python 3.14 ke liye MainThread par event loop manually set karein (import se pehle)
try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

from bot import Bot
import pyrogram.utils

pyrogram.utils.MIN_CHANNEL_ID = -1009147483647

if __name__ == "__main__":
    Bot().run()
    
