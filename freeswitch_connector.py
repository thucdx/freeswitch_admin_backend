import ESL


class Monitor:
    con = ESL.ESLconnection('fsexp', '8021', 'ClueCon')

    def __init__(self):
        if Monitor.con.connected():
            print 'Connected!,'
        else:
            print 'Not connected.'

    @staticmethod
    def command(cmd):
        print 'Send command: ', cmd
        return Monitor.con.api(cmd)

    @staticmethod
    def send_sms(to, msg):
        event = ESL.ESLevent("CUSTOM", "SMS::SEND_MESSAGE")
        event.addHeader('to', to)
        event.addHeader('from', 'sip:1019@35.165.245.123')
        event.addHeader('profile', 'public')
        event.addHeader('dest_proto', 'sip')
        event.addHeader('proto', 'sip')
        event.addBody(msg)

        Monitor.con.sendEvent(event)



