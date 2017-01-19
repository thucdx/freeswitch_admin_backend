import ESL


class Monitor:
    con = ESL.ESLconnection('fscent', '8021', 'ClueCon')

    def __init__(self):
        if Monitor.con.connected():
            print 'Connected!,'
        else:
            print 'Not connected.'

    @staticmethod
    def command(cmd):
        print 'Send command: ', cmd
        return Monitor.con.api(cmd)

    # to: user need to send message to. Please aware that it should be in format : extension@domain_ip
    # To be exact, you need to command: `sofia status profile internal reg` to view exact user address.
    @staticmethod
    def send_sms(to, msg):
        event = ESL.ESLevent('CUSTOM', 'SMS::SEND_MESSAGE')
        event.addHeader('to', to)
        event.addHeader('from', 'admin-tdx')
        event.addHeader('subject', 'message from admin')
        event.addHeader('profile', 'internal')
        event.addHeader('dest_proto', 'sip')
        event.addHeader('proto', 'sip')
        event.addHeader('hint', 'the hint')
        event.addHeader('replying', 'true')
        event.addHeader('type', 'text/plain')
        event.addBody(msg)

        Monitor.con.sendEvent(event)
        print event.serialize()

# Monitor.send_sms('1000@172.31.6.192', 'Hello from Freeswitch.')
