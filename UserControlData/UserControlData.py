
def set_run(ucd, input_value):
        if input_value == 't':
            ucd.run = True
        else:
            ucd.run = False


def set_speed(ucd, input_value):
    ucd.speed = int(float(input_value))


def set_turn(ucd, input_value):
    ucd.turn = int(float(input_value))

commands = {
    'set_run': set_run,
    'set_speed': set_speed,
    'set_turn': set_turn
            }


class UserControlData:
    def __init__(self):
        self.data = 'init'
        self.speed = 40
        self.turn = 90
        self.run = True

    def readInputString(self, input_str):
        command = input_str.split()
        print "Read input str: " + input_str
        if len(command) < 2:
            print 'err' #TODO handle
        else:
            commands[command[0]](self, command[1])


if __name__ == '__main__':
    print "Test code for user control data"
    d = UserControlData()
    d.readInputString('set_run f')
    assert (d.run is False), "Could not set_run to False"
    d.readInputString('set_speed 100')
    assert (d.speed == 100), "Could not set_speed to 100"
    d.readInputString('set_turn 100')
    assert (d.turn == 100), "Could not set_speed to 100"





