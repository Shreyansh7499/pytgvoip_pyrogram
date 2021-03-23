from stem.control import Controller
import io
import stem.process
from stem.util import term
import time, os, subprocess
import signal
import sys
import asyncio
from tgvoip import VoIPServerConfig
from tgvoip_pyrogram import VoIPFileStreamService, VoIPNativeIOService
import pyrogram

SOCKS_PORT = 9150
CONTROL_PORT = 9051
IN_CALL = True

ENTRY_F = '746DDCC32C78CFFA8A12C880FA15C28FF2988D6B'
MIDDLE_F = 'EBAC698FB36714DB60C5B8B2B9F2E1A18632C271'
EXIT_F = 'ED4325A6DB8D579CFF70F5A5630FD368464B0D64'


VoIPServerConfig.set_bitrate_config(80000, 100000, 60000, 5000, 5000)
client = pyrogram.Client(session_name = 'session', api_id=3263110, api_hash='23d1d90983308d7f77c67608d0b42664', proxy=dict(
        hostname="127.0.0.1",
        port=9150,
        username="",
        password=""))

loop = asyncio.get_event_loop()
voip_service = VoIPFileStreamService(client, receive_calls=False)



async def telegram_call():
    global IN_CALL
    await client.start()

    call = await voip_service.start_call('@poonamnagpal')
    call.play('audio_files/input.raw')
    call.play_on_hold(['audio_files/input.raw'])
    call.set_output_file('audio_files/output.raw')

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


def make_tor_circuit(controller):
	path = [ENTRY_F, MIDDLE_F, EXIT_F]
	circuit_id = controller.new_circuit(path, await_build = True)

	def attach_stream(stream):
		print(stream.status)
		if stream.status == 'NEW':
			controller.attach_stream(stream.id, circuit_id)
			print(stream.id, circuit_id)

	controller.add_event_listener(attach_stream, stem.control.EventType.STREAM)

	try:
		controller.set_conf('__LeaveStreamsUnattached', '1')  # leave stream management to us
		loop.run_until_complete(telegram_call())

	except Exception as e:
		print(f"Exception {e}")
	finally:
		controller.remove_event_listener(attach_stream)
		controller.reset_conf('__LeaveStreamsUnattached')
		controller.close_circuit(circuit_id)
    
if __name__ == '__main__':
    
	with Controller.from_port(port = CONTROL_PORT) as controller:
		controller.authenticate()
		controller.set_conf("MaxCircuitDirtiness", "2592000")
		controller.set_conf("NewCircuitPeriod", "2592000")

		make_tor_circuit(controller)
