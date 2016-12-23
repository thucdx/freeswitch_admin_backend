from flask import Flask, jsonify
import jsonpickle
from expiringdict import ExpiringDict

from conference import Conference

bookingConference = ExpiringDict(max_len=100, max_age_seconds=10)

app = Flask(__name__)
app.url_map.strict_slashes = False

OK = {'status': 'OK'}
GENERAL_ERROR = {'status': 'ERROR'}
NOT_FOUND = {'result': 'NOT FOUND'}


def jsonpickerencode(func):
    def func_wrapper(*args, **kwargs):
        return jsonpickle.encode(func(*args, **kwargs))
    return func_wrapper


@app.route('/status', methods=['GET'])
def get():
    return jsonify({'status': 'works!'})


@app.route('/conferences', methods=['GET'])
def get_conference_list():
    conf = Conference.get_conference_list()
    if conf:
        return jsonpickle.encode(conf)
    else:
        return jsonpickle.encode({'status': 'not found'})


@app.route('/conferences/<conf_name>', methods=['GET'])
def get_conference_info(conf_name):
    print 'conf_name', conf_name
    return jsonpickle.encode(Conference.get_by_name(conf_name))


@app.route('/conferences/<conf_name>/admin/<admin>', methods=['POST'])
def set_admin(conf_name, admin):
    conference = Conference.get_by_name(conf_name)
    if conference:
        conference.set_admin(admin)
        return jsonpickle.encode(OK)
    else:
        return jsonpickle.encode({'status': 'Conference not found!'})


@app.route('/conferences/<conf_name>/<viewer>/<viewee>', methods=['POST'])
def set_admin_view(conf_name, viewer, viewee):
    conference = Conference.get_by_name(conf_name)
    if conference:
        conference.set_view_by_number(viewer, viewee)
        return jsonpickle.encode(OK)
    else:
        return jsonpickle.encode({'status': 'Conference not found!'})


@app.route('/conferences/free', methods=['GET'])
def get_available_conference():
    active_confererences = Conference.get_conference_list()
    for room in range(3000, 3100):
        ok = True
        room_str = str(room)

        for conf in active_confererences:
            if conf.name.startswith(room_str):
                ok = False
                break
        if ok and room_str not in bookingConference:
            bookingConference[room_str] = 1
            return jsonpickle.encode({'result': room_str})

    return jsonpickle.encode(NOT_FOUND)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
