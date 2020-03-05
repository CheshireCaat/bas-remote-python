import asyncio

from bas_remote import BasRemoteClient
from bas_remote import Options


async def main():
    client = BasRemoteClient(options=Options(script_name='TestRemoteControl'))

    await client.start()

    result = await client.run_function('GoogleSearch', {'Query': 'cats'})

    for link in result:
        print(link)

    await client.close()


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(main())
