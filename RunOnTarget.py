import paramiko

import paramiko, base64



class Target:
    def __init__(self):
        self.hostname = '192.168.0.104'
        self.username = 'pi'
        self.password = 'raspberry'
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())

    def start(self):
        self.client.connect(self.hostname, port=22, username=self.username, password=self.password)
        self.client.invoke_shell()

    def run(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        print 'Output: '
        for line in stdout:
            print '... ' + line.strip('\n')
        print 'Errors: '
        for line in stderr:
            print '... ' + line.strip('\n')

    def stop(self):
        self.client.close()

if __name__ == '__main__':
    #target = Target()
    #target.start()
    #target.run('python LegoRover/Sensors/RangeSensor_new_interrupt_based.py')
    #target.run('python LegoRover/Tgtest/SendData.py')
    #target.stop()




