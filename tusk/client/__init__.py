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
        self.ref = weakref.proxy(self) # use weakref when handling requests
    
    def data_received(self, data):
        self.data += data  # Append new data to existing data
        
        messages = re.split(b'\r\n|\x00', self.data)
        self.data = messages.pop()  # Save any incomplete message for next time
        
        for message in messages:
            asyncio.create_task(self.handle_message(message))

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        self.server.logger.debug(f'Connection from {peername}')
        self.transport = transport

    async def handle_message(self, message):
        if message.startswith('<'):
            self.send_line('<cross-domain-policy><allow-access-from domain="*" to-ports="*"/>', '\x00')
            return self.close()
        packet_split = message.split()
        cmd = packet_split[0]
        if cmd.startswith('/'):
            handlers = slash_command_handlers[cmd[1:]]
            
        if self.place is not None:
            if cmd in inputs[self.place]:
                handlers = inputs[self.place][cmd]
            # TODO: SWF CROSSWORLD COMMAND HANDLING
    
        for handler in handlers:
            try:
                await handler(self.ref, *packet_split[1:])
            except:
                # TODO: error handling
                pass

    def connection_lost(self, exc):
        for handler in server_handlers['disconnected']:
            asyncio.create_task(handler(self.ref))
            
        if self.user is not None:
            del self.server.penguins_by_id[self.user.id]
    
    async def send_tag(self, tag, *data):
        data = '|'.join(map(str, data))
        self.transport.write(f'[{tag}]|{data}')
        
    def send_line(self, data, delimiter='\r\n'):
        if not self.transport.is_closing():
            self.server.logger.debug(f'Outgoing data: {data}')
            self.transport.write((data + delimiter).encode())

    def close(self):
        # Clear buffer
        self.data = b''
        self.transport.close()
