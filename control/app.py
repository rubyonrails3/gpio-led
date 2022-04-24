import asyncio
import gpiod
from datetime import datetime
from suntime import Sun
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from .sysfs import Sysfs

class Backend(ApplicationSession):
    user_intervene = False
    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)

    def onConnect(self):
        self.join(self.config.realm)

    async def onJoin(self, _):
        print('Connected with router')
        self.led = self.__request_line(2)
        await self.register(self.current_state, 'com.lights.current_state')
        await self.register(self.accept_command, 'com.lights.change_state')
        while True:
            if Backend.user_intervene == False:
                self.manage_lights()
            else:
                print('Intervened...')

            await asyncio.sleep(5)

    async def onDisconnect(self):
        print('Disconnnecting...')
        asyncio.get_event_loop().stop()

    def current_state(self):
        return 'on' if self.led.get_value() == 0 else 'off'

    def accept_command(self, state = 'off'):
        Backend.user_intervene = False if state == 'reset' else True
        if state == 'reset':
            self.manage_lights()
        else:
            self.update_light(state)

    def update_light(self, state = 'off'):
        did_state_change = False
        if self.current_state() == 'off' and state == 'on':
            self.led.set_value(0)
            did_state_change = True
        elif self.current_state() == 'on' and state == 'off':
            self.led.set_value(1)
            did_state_change = True

        if did_state_change:
            self.publish('com.lights.update', self.current_state())

        return self.current_state()

    def manage_lights(self):
        latitude = 30.181459
        longitude = 71.492157

        sun = Sun(latitude, longitude)

        now = datetime.now().time()
        today_sunrise = sun.get_local_sunrise_time().time()
        today_sunset = sun.get_local_sunset_time().time()
        if today_sunrise < now and today_sunset > now:
            self.update_light('off')
        else:
            self.update_light('on')


    def __request_line(self, number):
        print('Requesting Line')
        try:
            chip = gpiod.chip(0)
            led = chip.get_line(number)

            config = gpiod.line_request()
            config.consumer = 'Blink'
            config.request_type = gpiod.line_request.DIRECTION_OUTPUT

            led.request(config)
            return led
        except:
            print('Failed to connect to Chip, trying SysFS')
            return Sysfs(number)


if __name__ == '__main__':
    url     = 'ws://ec2-3-133-149-135.us-east-2.compute.amazonaws.com:8080/ws'
    realm   = 'realm1'
    runner  = ApplicationRunner(url, realm)
    runner.run(Backend)
