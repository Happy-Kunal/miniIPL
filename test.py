import asyncio
import aiohttp
import matchInfo
import poll
import time
async def main():
    session = aiohttp.ClientSession()
    question = "testing the poll"
    options = ["poll tes1", "test2"]
    close_time = time.time() + 3600
    await poll.send_poll(session, question, options, close_time)
    await session.close()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
