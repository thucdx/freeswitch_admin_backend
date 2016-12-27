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

    def is_admin(self):
        return self.status is not None and self.status.find('moderator') >= 0
