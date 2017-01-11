import re
import user

from freeswitch_connector import Monitor


class Conference:
    NO_CONFERENCE = "No active conferences."
    HEADER_PATTERN = "Conference (\S+) \((\d+) member(s*) rate: (\d+) flags: ([\w|]+)\)"
    UNKNOWN_ID = '-1'

    RELATION_CLEAR = 'clear'
    RELATION_SENDVIDEO = 'sendvideo'

    def __init__(self, name='noname', total=0, rate=-1, flags=''):
        self.name = name
        self.total = total
        self.users = []
        self.flags = flags
        self.rate = rate

    def add_user(self, user):
        self.users.append(user)

    def get_users(self):
        return self.users

    def find_id_by_number(self, number):
        for u in self.get_users():
            if u.caller_number == number:
                return u.id
        return Conference.UNKNOWN_ID

    def set_admin(self, number):
        pass

    def get_normal_user_ids(self):
        return [u.id for u in self.users if not u.is_admin()]

    def get_admin_ids(self):
        return [u.id for u in self.users if u.is_admin()]

    # admin should see member, while normal user see each other
    def init_monitoring(self):
        admin_ids = self.get_admin_ids()
        normal_user_ids = self.get_normal_user_ids()
        print 'admin_ids', admin_ids
        print 'normal_user_ids', normal_user_ids

        if len(normal_user_ids) < 2:
            print '!!!!!!!!! It might not work properly due to total number of user is %s' % len(normal_user_ids)

        if len(normal_user_ids) == 2 and len(admin_ids) > 0:

            # clear relation from admin to normal user. So admin would not send video /voice to normal user
            for u in normal_user_ids:
                self.relate(",".join(admin_ids), u, Conference.RELATION_CLEAR)

            # clear relation from normal user to admin. So we can freely choose which user's video admin should see
            for a in admin_ids:
                self.relate(",".join(normal_user_ids), a, Conference.RELATION_CLEAR)

            # set view for admin - Round robin
            index = 0
            for a in admin_ids:
                self.relate(normal_user_ids[index], a, Conference.RELATION_SENDVIDEO)
                index = (index + 1) % len(normal_user_ids)
                # default to no hear
                # self.undeaf(a)

            # member seeing each other
            for u in normal_user_ids:
                self.relate(','.join(normal_user_ids), u, Conference.RELATION_CLEAR)

            index = 0
            for i in range(len(normal_user_ids)):
                nxt = (index + 1) % len(normal_user_ids)
                self.relate(normal_user_ids[index], normal_user_ids[nxt], Conference.RELATION_SENDVIDEO)
                index = nxt

    # admin A should see B
    def set_admin_view(self, admin_number, normal_user_number):
        admin_id = self.find_id_by_number(admin_number)
        user_id = self.find_id_by_number(normal_user_number)

        if admin_id == Conference.UNKNOWN_ID or user_id == Conference.UNKNOWN_ID:
            print 'Unknown number. Please check again'
            return

        admin_ids = self.get_admin_ids()
        user_ids = self.get_normal_user_ids()

        if admin_id not in admin_ids or user_id not in user_ids:
            print 'Invalid command!'
            return

        # clear relation from other user to admin
        self.relate(','.join(user_ids), admin_id, Conference.RELATION_CLEAR)

        # user send video to admin
        self.relate(user_id, admin_id, Conference.RELATION_SENDVIDEO)

        # allow admin to hear
        # default to no hear
        # self.undeaf(admin_id)

        # member seeing each other
        for u in user_ids:
            self.relate(','.join(user_ids), u, Conference.RELATION_CLEAR)

        index = 0
        for i in range(len(user_ids)):
            nxt = (index + 1) % len(user_ids)
            self.relate(user_ids[index], user_ids[nxt], Conference.RELATION_SENDVIDEO)
            index = nxt

    def set_admin_hear(self, admin_number, can_hear):
        admin_id = self.find_id_by_number(admin_number)
        if can_hear:
            self.undeaf(admin_id)
        else:
            self.deaf(admin_id)

    def set_view_by_id(self, active_id, inactive_id):
        pass

    def relate(self, id, other_id, relation):
        Monitor.command('conference %s relate %s %s %s' % (self.name, id, other_id, relation))

    def undeaf(self, id):
        Monitor.command('conference %s undeaf %s' % (self.name, id))

    def deaf(self, id):
        Monitor.command('conference %s deaf %s' % (self.name, id))

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
        conf_list = Monitor.command('conference list')
        if conf_list:
            str = conf_list.getBody()
            return Conference.from_string(str)
        else:
            return []
