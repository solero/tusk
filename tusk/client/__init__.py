from tusk.managers.object import ObjectManager
from tusk.handlers import slash_command_handlers, server_handlers
from tusk.places import inputs

import re
import weakref
import asyncio
class MetaplaceServerProtocol(asyncio.Protocol):

    
    def __init__(self, server):
        super().__init__()
        self.server = server
        self.data = b''  # Keep track of received data
        self.user_events = {}
        self.crossworld_ui = False
        self.window_manager = None
        self.place = None
        self.user = None
        self.element = None
        self.context = {}
        self.ref = weakref.proxy(self) # use weakref when handling requests
        self.objects = ObjectManager(self.ref)

    def get_url(self, url: str = ''):
        return self.context['base_asset_url'] + url
    
    def data_received(self, data):
        self.data += data  # Append new data to existing data
        messages = re.split(b'\r\n|\x00', self.data)
        self.data = messages.pop()  # Save any incomplete message for next time
        
        for message in messages:
            asyncio.create_task(self.handle_message(message.decode()))

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        self.server.logger.debug(f'Connection from {peername}')
        self.transport = transport

    async def handle_message(self, message):
        self.server.logger.debug(f'Handling data {message}')
        if message.startswith('<'):
            self.send_line('<cross-domain-policy><allow-access-from domain="*" to-ports="*"/></cross-domain-policy>', '\x00')
            return self.close()
        packet_split = message.split()
        cmd = packet_split[0]

        handlers = None
        if cmd.startswith('/'):
            handlers = slash_command_handlers.get(cmd[1:])
            
        if self.place is not None:
            if cmd in inputs.get(self.place.name, {}):
                handlers = inputs.get(self.place.name, {}).get(cmd)
            elif cmd in self.user_events:
                handlers = self.user_events.get(cmd)

        if handlers is None:
            self.server.logger.debug(f'Handler for {message} does not exist!')
            return

        for handler in handlers:
            try:
                await handler.callback(self.ref, *packet_split[1:])
            except Exception as e:
                print(e)
                # TODO: error handling
                pass

    def connection_lost(self, exc):

        peername = self.transport.get_extra_info('peername')
        self.server.logger.info(f'{peername} Disconnected')

        for handler in server_handlers['disconnected']:
            asyncio.create_task(handler(self.ref))
        
        if self.user is not None:
            if self.user.id in self.server.penguins_by_id:
                del self.server.penguins_by_id[self.user.id]
            self.user = None
            self.place = None
            self.window_manager = None
            self.server = None
    
    async def send_tag(self, tag, *data):
        data = '|'.join(map(str, data))
        self.send_line(f'[{tag}]|{data}')
        
    def send_line(self, data, delimiter='\r\n'):
        if not self.transport.is_closing():
            self.server.logger.debug(f'Outgoing data: {data}')
            self.transport.write((data + delimiter).encode())

    def close(self):
        # Clear buffer
        self.data = b''
        self.transport.close()
