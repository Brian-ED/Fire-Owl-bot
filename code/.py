import asyncio

async def hello():
    print('Hello ...')
    await asyncio.sleep(5)
    print('... World!')

async def main():
    await asyncio.gather(hello(), hello())

asyncio.run(main())