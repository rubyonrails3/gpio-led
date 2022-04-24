from .app import Backend
from autobahn.asyncio.wamp import ApplicationRunner

def start():
    url     = 'ws://ec2-3-133-149-135.us-east-2.compute.amazonaws.com:8080/ws'
    realm   = 'realm1'
    runner  = ApplicationRunner(url, realm)
    runner.run(Backend)

