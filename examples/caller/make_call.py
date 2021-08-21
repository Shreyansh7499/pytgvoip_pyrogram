import asyncio
from config import *
from tgvoip import VoIPServerConfig
from tgvoip_pyrogram import VoIPFileStreamService, VoIPNativeIOService
import pyrogram
from pathlib import Path
import os

BASE_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
VoIPServerConfig.set_bitrate_config(80000, 100000, 60000, 5000, 5000)
client = pyrogram.Client(session_name = 'session', api_id=API_ID, api_hash=API_HASH, proxy=dict(
        hostname="127.0.0.1",
        port=9050,
        username="",
        password=""))

loop = asyncio.get_event_loop()
voip_service = VoIPFileStreamService(client, receive_calls=False)

IN_CALL = True

async def telegram_call(num_call):
    global IN_CALL
    await client.start()

    call = await voip_service.start_call('@shreyansh7499')
    call.play(str(BASE_DIR / 'audio_files/input.raw'))
    call.play_on_hold([str(BASE_DIR / 'audio_files/input.raw')])
    call.set_output_file(f'{str(BASE_DIR)}/audio_files/recordings/output{str(num_call)}.raw')

    @call.on_call_state_changed
    def state_changed(call, state):
        print('State changed:', call, state)

    @call.on_call_ended
    async def call_ended(call):
        global IN_CALL
        await asyncio.sleep(2)
        await client.stop()
        IN_CALL = False

    while IN_CALL:
        await asyncio.sleep(1)

loop.run_until_complete(telegram_call(1))