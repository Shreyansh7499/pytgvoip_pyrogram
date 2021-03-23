import asyncio
from .config import *
import pyrogram
from tgvoip import VoIPServerConfig
from tgvoip_pyrogram import VoIPFileStreamService, VoIPIncomingFileStreamCall,\
    VoIPNativeIOService, VoIPIncomingNativeIOCall

VoIPServerConfig.set_bitrate_config(80000, 100000, 60000, 5000, 5000)
client = pyrogram.Client(session_name = 'session', api_id=API_ID, api_hash=API_HASH, proxy=dict(
        hostname="127.0.0.1",
        port=9150,
        username="",
        password=""))

loop = asyncio.get_event_loop()
service = VoIPFileStreamService(client)  # use VoIPNativeIOService for native I/O


@service.on_incoming_call
async def process_call(call: VoIPIncomingFileStreamCall):  # use VoIPIncomingNativeIOCall for native I/O
    await call.accept()
    call.play('audio_files/input.raw')
    call.play_on_hold(['audio_files/input.raw'])
    call.set_output_file('audio_files/output.raw')

    # you can use `call.on_call_ended(lambda _: app.stop())` here instead
    @call.on_call_ended
    async def call_ended(call):
        await client.stop()

loop.run_until_complete(client.run())
