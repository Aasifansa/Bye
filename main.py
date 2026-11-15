import asyncio

# Python ke event loop ke liye
try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

from bot import Bot
import pyrogram.utils
import cbb  # 👈 Ye zaroori hai taaki buttons (cbb.py) load ho sakein

pyrogram.utils.MIN_CHANNEL_ID = -1009147483647

if __name__ == "__main__":
    Bot().run()
    
