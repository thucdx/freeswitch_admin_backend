import re
import user

from freeswitch_connector import Monitor


class Conference:
    NO_CONFERENCE = "No active conferences."
    HEADER_PATTERN = "Conference (\S+) \((\d+) member(s*) rate: (\d+) flags: ([\w|]+)\)"
    UNKNOWN_ID = '-1'

    def __init__(self, name='noname', total=0, rate=-1, flags=''):
        self.name = name
        self.total = total
        self.users = []
        self.admin_ids = []
        self.flags = flags
        self.rate = rate

    def add_user(self, user):
        self.users.append(user)

    def get_users(self):
        return self.users

    def find_id_by_number(self, number):
        for user in self.get_users():
            if user.caller_number == number:
                return user.id
        return Conference.UNKNOWN_ID

    def set_admin(self, number):
        admin_id = self.find_id_by_number(number)
        print 'total user', self.total

        if admin_id != Conference.UNKNOWN_ID:
            if admin_id not in self.admin_ids:
                self.admin_ids.append(admin_id)

            # clear view of member
            user_ids = self.get_normal_users()

            # IMPORTANT ASSUMPTION: assume total normal user is 2
            for user_id in user_ids:
                for admin_id in self.admin_ids:
                    Monitor.command('conference %s relate %s %s clear' % (self.name, admin_id, user_id))
                    Monitor.command('conference %s relate %s %s clear' % (self.name, user_id, admin_id))

            if len(user_ids) == 2:
                Monitor.command('conference %s relate %s %s sendvideo' % (self.name, user_ids[0], user_ids[1]))
                Monitor.command('conference %s relate %s %s sendvideo' % (self.name, user_ids[1], user_ids[0]))
            else:
                print("!!!!!!!!! total normal user is not 2  !!!!!")

            # set default view for admin
            if len(user_ids) > 0:
                for admin_id in self.admin_ids:
                    Monitor.command('conference %s relate %s %s sendvideo' % (self.name, user_ids[0], admin_id))

    def get_normal_users(self):
        user_ids = []
        for user in self.get_users():
            if user.id not in self.admin_ids:
                user_ids.append(user.id)
        print 'total normal user: ', len(user_ids)
        return user_ids

    def set_admin_view(self, inactive_number):
        inactive_id = self.find_id_by_number(inactive_number)

        for admin_id in self.admin_ids:
            self.set_view_by_id(admin_id, inactive_id)

    # A see B, in otherwords: B send video to A
    def set_view_by_number(self, active_number, inactive_number):
        current_active_id = self.find_id_by_number(active_number)
        current_inactive_id = self.find_id_by_number(inactive_number)

        if current_active_id == Conference.UNKNOWN_ID or current_inactive_id == Conference.UNKNOWN_ID:
            print 'Invalid command'
            return
        self.set_view_by_id(current_active_id, current_inactive_id)

    def set_view_by_id(self, active_id, inactive_id):
        user_ids = self.get_normal_users()

        # for user_id in user_ids:
        Monitor.command('conference %s relate %s %s clear' % (self.name, ','.join(user_ids), active_id))
        for user_id in user_ids:
            Monitor.command('conference %s relate %s %s clear' % (self.name, active_id, user_id))

        Monitor.command('conference %s relate %s %s sendvideo' % (self.name, inactive_id, active_id))

    @staticmethod
    def get_by_name(conf_name):
        all = Conference.get_conference_list()
        if len(all) > 0:
            for conf in all:
                if conf.name.startswith(conf_name):
                    return conf
        return None

    @staticmethod
    def from_string(conference_as_string):
        lines = conference_as_string.split('\n')
        conference_list = []
        id = 0

        while id < len(lines):
            header = lines[id]
            conference = Conference.from_header(header)
            id += 1

            if conference:
                for i in range(conference.total):
                    u = user.User.parse(lines[id])
                    conference.add_user(u)
                    # print user, i, id
                    id += 1
                conference_list.append(conference)
            else:
                break

        return conference_list

    @staticmethod
    def from_header(header_as_string):
        if header_as_string.find(Conference.NO_CONFERENCE) < 0:
            m = re.match(Conference.HEADER_PATTERN, header_as_string)
            if m:
                t = m.groups()
                name, total, rate, flags = t[0], int(t[1]), int(t[3]), t[4]
                # print 'parse: ', name, total, rate, flags
                return Conference(name, total, rate, flags)
        return None

    @staticmethod
    def get_conference_list():
        str = Monitor.command('conference list').getBody()
        return Conference.from_string(str)
