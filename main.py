from bas_remote.callback import ClientCallback
from bas_remote.client import BasRemoteClient
from bas_remote.options import Options
import asyncio


class DefCallback(ClientCallback):

    async def on_message_received(self, message):
        print('<---', message)

    async def on_message_sent(self, message):
        print('--->', message)


async def main(loop):
    def on_variable_get(data):
        print('get ok')
        print(data)

    def on_variable_set():
        print('set ok')

    client = BasRemoteClient(
        Options(scriptName='TestRemoteControl'), DefCallback(), loop)
    await client.start()
    print('here')
    await client.send_async('set_global_variable', {
        'name': 'TEST',
        'value': 5
    }, on_variable_set)
    await asyncio.sleep(2)
    await client.send_async('get_global_variable', {
        'name': 'TEST'
    }, on_variable_get)

    while (True):
        try:
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
