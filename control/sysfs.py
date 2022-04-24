import os
class Sysfs:
    GPIO_SYSFS_PATH = '/sys/class/gpio/gpio'
    def __init__(self, pin):
        self.pin = pin
        self.path = "{}{}".format(self.GPIO_SYSFS_PATH, pin)
        if not os.path.exists(self.path):
            print('Invalid GPIO pin: {}'.format(self.pin))
            exit(1)

    def set_value(self, number):
        with open("{}/direction".format(self.path), 'w') as file:
            file.write('out')

        with open("{}/value".format(self.path), 'w') as file:
            file.write("{}".format(number))


    def get_value(self):
        with open("{}/value".format(self.path), 'r') as file:
            value = file.readline()
            if value:
                return int(value)
