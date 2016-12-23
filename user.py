class User:
    def __init__(self, id, register_string, uuid, caller_name, caller_number, status,
                 volume_setting, energy, volume_out, energy_setting):
        self.id = id
        self.register_string = register_string
        self.uuid = uuid
        self.caller_name = caller_name
        self.caller_number = caller_number
        self.status = status
        self.volume_setting = volume_setting
        self.energy = energy
        self.volume_out = volume_out
        self.energy_setting = energy_setting

    @staticmethod
    def parse(user_as_string):
        id, register_string, uuid, caller_name, caller_number, \
        status, volume_setting, energy, volume_out, energy_setting = user_as_string.split(";")

        return User(id, register_string, uuid, caller_name, caller_number, \
                    status, volume_setting, energy, volume_out, energy_setting)


#
# user = User.parse("5;sofia/internal/1002@35.165.245.123;76245f95-50fe-48a4-bb2a-4cbeb9bf295b;1002;1002;hear|speak|video|floor|vid-floor;0;0;0;100")
# print user.id, user.status