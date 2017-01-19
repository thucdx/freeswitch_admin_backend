from freeswitch_connector import Monitor as m


def invite(room_name, extension):
    new_uuid = m.command('create_uuid')
    print new_uuid.getBody()

    originate_command = 'bgapi originate {origination_uuid=%s}user/%s &conference(%s)}' % (new_uuid.getBody(), extension, room_name)
    print originate_command
    originate_result = m.command(originate_command)
    print originate_result.getBody()

# Besure 1015 is connected via TCP. UDP does not work.
# invite('3000-172.31.6.192', '1015')
