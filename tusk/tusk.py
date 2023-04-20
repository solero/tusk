import asyncio
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from tusk.handlers import server_handlers, get_package_modules
from tusk.client import MetaplaceServerProtocol
from tusk.api.app import app

import tusk.handlers
import tusk.places

import weakref
try:
    import uvloop
    uvloop.install()
except ImportError:
    uvloop = None

#never gonna give you up, never gonna let you downnn, never gonna run around and desert youuu!

class Tusk:

    def __init__(self, id, owner, name):
        self.server = None
        self.server_coroutine = None
        
        self.id = id
        self.owner = owner
        self.name = name
        self.redis = app.redis
        self.penguins_by_id = {}

        self.stylesheet_id = '87.5309'

        self.port = None

        self.items = None
        self.stamps = None
        self.cards = None
        self.ref = weakref.proxy(self)

    def init_logger(self):
        general_log_file = f'logs/{self.name}-general.log'
        errors_log_file = f'logs/{self.name}-errors.log'
        general_log_directory = os.path.dirname(general_log_file)
        errors_log_directory = os.path.dirname(errors_log_file)
        if not os.path.exists(general_log_directory):
            os.mkdir(general_log_directory)
        if not os.path.exists(errors_log_directory):
            os.mkdir(errors_log_directory)

        self.logger = logging.getLogger(self.name)
        universal_handler = RotatingFileHandler(general_log_file,
                                                maxBytes=2097152, backupCount=3, encoding='utf-8')

        error_handler = logging.FileHandler(errors_log_file)
        console_handler = logging.StreamHandler(stream=sys.stdout)

        log_formatter = logging.Formatter(f'%(asctime)s [{self.name}] [%(levelname)-5.5s]  %(message)s')
        error_handler.setLevel(logging.ERROR)

        universal_handler.setFormatter(log_formatter)
        console_handler.setFormatter(log_formatter)

        self.logger.addHandler(universal_handler)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(error_handler)

        level = logging.getLevelName('DEBUG')
        self.logger.setLevel(level)

    async def start(self):
        if self.server is not None:
            return
        self.init_logger()
        loop = asyncio.get_running_loop()
        self.server = await loop.create_server(lambda: MetaplaceServerProtocol(self.ref), '0.0.0.0', 0)
        host, self.port = self.server.sockets[0].getsockname()
        self.logger.info('Booting Tusk')
        self.logger.info('Tusk server started')
        
        for handler in server_handlers['boot']:
            try:
                await handler(self.ref)
            except:
                pass
                
        self.logger.info(f'Listening on {host}:{self.port}')
        self.server_coroutine = asyncio.create_task(self.server.serve_forever())

