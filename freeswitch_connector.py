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
        return Monitor.con.api(cmd)




