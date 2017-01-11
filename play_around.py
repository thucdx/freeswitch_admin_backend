from freeswitch_connector import Monitor

con = Monitor.con
while con.connected:
    # con.events('plain', 'CHANNEL_ANSWER')
    # con.events('plain', 'CHANNEL_HANGUP')
    con.events('plain', 'CHANNEL_ANSWER')
    con.events('plain', 'CHANNEL_HANGUP_COMPLETE')
    while 1:
        e = con.recvEvent()
        if e:
            print e.serialize()
