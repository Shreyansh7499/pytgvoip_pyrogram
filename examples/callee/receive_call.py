import asyncio
from config import *
import pyrogram
from tgvoip import VoIPServerConfig
from tgvoip_pyrogram import VoIPFileStreamService, VoIPIncomingFileStreamCall, VoIPNativeIOService, VoIPIncomingNativeIOCall
from pathlib import Path
import os


BASE_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
NUM_CALLS = 0
VoIPServerConfig.set_bitrate_config(80000, 100000, 60000, 5000, 5000)
client = pyrogram.Client(session_name = 'session', api_id=API_ID, api_hash=API_HASH)
loop = asyncio.get_event_loop()
service = VoIPFileStreamService(client)  # use VoIPNativeIOService for native I/O


@service.on_incoming_call
async def process_call(call: VoIPIncomingFileStreamCall):  # use VoIPIncomingNativeIOCall for native I/O
    global NUM_CALLS
    await call.accept()
    call.play(str(BASE_DIR / 'audio_files/input.raw'))
    call.play_on_hold([str(BASE_DIR / 'audio_files/input.raw')])
    call.set_output_file(f'{str(BASE_DIR)}/audio_files/recordings/output{str(NUM_CALLS)}.raw')
    NUM_CALLS += 1

    @call.on_call_ended
    async def call_ended(call):
        pass

loop.run_forever(client.run())

