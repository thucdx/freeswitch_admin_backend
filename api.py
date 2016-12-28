from flask import Flask, jsonify, request
from flask_cors import CORS

import jsonpickle
# import json
from expiringdict import ExpiringDict

from conference import Conference

RESERVED_TIME = 35
reservedConference = ExpiringDict(max_len=100, max_age_seconds=RESERVED_TIME)
bookingConference = ExpiringDict(max_len=1000, max_age_seconds=RESERVED_TIME)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.url_map.strict_slashes = False

OK = {'status': 'OK'}
GENERAL_ERROR = {'status': 'ERROR'}
NOT_FOUND = {'result': 'NOT FOUND'}


def available_conference():
    active_confererences = Conference.get_conference_list()
    for room in range(3000, 3100):
        ok = True
        room_str = str(room)

        for conf in active_confererences:
            if conf.name.startswith(room_str):
                ok = False
                break
        if ok and room_str not in reservedConference:
            return room_str
    return ''


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
        return jsonpickle.encode([])


@app.route('/conferences/<conf_name>', methods=['GET'])
def get_conference_info(conf_name):
    print 'conf_name', conf_name
    conf_detail = Conference.get_by_name(conf_name)
    if conf_detail:
        return jsonpickle.encode(conf_detail)
    else:
        return jsonpickle.encode(NOT_FOUND)


@app.route('/conferences/<conf_name>/init', methods=['POST'])
def set_admin(conf_name):
    conference = Conference.get_by_name(conf_name)
    if conference:
        conference.init_monitoring()
        return jsonpickle.encode(OK)
    else:
        return jsonpickle.encode({'status': 'Conference not found!'})


@app.route('/conferences/call', methods=['POST'])
def book_room():
    # get and validate
    print 'Request data', request.data

    try:
        data = jsonpickle.loads(request.data)
    except:
        return jsonpickle.encode({'code': -1, 'data': {'message': 'invalid json', 'data': request.data}})

    if 'caller' not in data or 'callee' not in data:
        return jsonpickle.encode({'code': -1, 'data': {'message': 'invalid json'}})

    caller = data['caller']
    callee = data['callee']

    # check if call has been booked!
    if (caller, callee) in bookingConference:
        room_str = bookingConference.get((caller, callee))
        return jsonpickle.encode({'code': 0, 'data': {'room': room_str}})
    else:
        room_str = available_conference()
        if room_str != '':
            bookingConference[(caller, callee)] = room_str
            bookingConference[(callee, caller)] = room_str
            reservedConference[room_str] = 1
            return jsonpickle.encode({'code': 0, 'data': {'room': room_str}})
        else:
            return jsonpickle.encode({'code': -1, 'data': {}})


@app.route('/conferences/<conf_name>/<viewer>/<viewee>', methods=['POST'])
def set_admin_view(conf_name, viewer, viewee):
    conference = Conference.get_by_name(conf_name)
    if conference:
        conference.set_admin_view(viewer, viewee)
        return jsonpickle.encode(OK)
    else:
        return jsonpickle.encode({'status': 'Conference not found!'})


@app.route('/conferences/free', methods=['GET'])
def get_available_conference():
    room_str = available_conference()
    if room_str != '':
        reservedConference[room_str] = 1
        return jsonpickle.encode({'code': 0, 'data': {'room': room_str}})
    else:
        return jsonpickle.encode({'code': -1, 'data': {}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
