import datetime
import json

from flask import Flask, request, jsonify
from flask_caching import Cache

from models.enums.building_key import CHOICES as BUILDING_KEY_CHOICES, BuildingKey
from models.enums.faculty import CHOICES as FACULTY_CHOICES, Faculty
from utils.allocation_controller import UnivISAllocationController
from utils.controllers import UnivISLectureController
from utils.room_controller import UnivISRoomController

API_V1_ROOT = "/api/v1/"
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


def make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    return (path + args)


@app.route(f'{API_V1_ROOT}/')
def hello():
    return "Hello World!"


@app.route(f'{API_V1_ROOT}lectures/', methods=['GET'])
def lectures():
    search_token = request.args.get('token', None)
    if search_token:
        univis_lecture_c = UnivISLectureController()
        lectures = univis_lecture_c.get_lectures_by_token(search_token)
        if lectures:
            # lectures_after, lectures_before = univis_lecture_c.get_lectures_split_by_date(lectures)
            # lectures_dict = {'before': lectures_before, 'after': lectures_after}
            # lectures_dict['before'] = get_lectures_as_dicts(lectures_dict['before'])
            # lectures_dict['after'] = get_lectures_as_dicts(lectures_dict['after'])
            return jsonify(json.dumps(lectures, default=lambda o: o.__dict__ if not isinstance(o, (
                datetime.date, datetime.datetime)) else o.isoformat(), indent=4))
        else:
            return jsonify(status_code=204)
    else:
        return jsonify(status_code=400)


@app.route(f'{API_V1_ROOT}rooms/', methods=['GET'])
@cache.cached(timeout=86400, key_prefix=make_cache_key)
def rooms():
    search_token = request.args.get('token', None)
    name = request.args.get('name', None)
    long_name = request.args.get('token', None)
    size = request.args.get('size', None)
    id = request.args.get('id', None)
    # TODO: all departments
    # department = request.args.get('faculty', None)
    faculty = request.args.get('faculty', None)
    building_keys = request.args.getlist('building_keys', None)

    univis_room_c = UnivISRoomController()
    if search_token or name or long_name or size or id or faculty or building_keys:
        faculty_enum = get_enum(Faculty, faculty) if faculty else None
        building_key_enums = [get_enum(BuildingKey, building_key) for building_key in building_keys if building_key]
        rooms = []
        for building_key_enum in building_key_enums:
            url = univis_room_c.get_univis_api_url(search_token, name, long_name, size, id, faculty_enum,
                                                   building_key_enum)
            rooms.extend(univis_room_c.get_rooms(url))
    else:
        rooms = univis_room_c.get_rooms()
    room_dicts = [room.__dict__ for room in rooms]
    return jsonify(room_dicts)


@app.route(f'{API_V1_ROOT}allocations/', methods=['GET'])
@cache.cached(timeout=86400, key_prefix=make_cache_key)
def allocations():
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)
    start_time = request.args.get('start_time', None)
    end_time = request.args.get('end_time', None)

    if start_date or end_date or start_time or end_time:
        univis_alloc_c = UnivISAllocationController()
        allocations = univis_alloc_c.get_filtered_allocations(start_date, end_date, start_time, end_time)
        return jsonify(json.loads(json.dumps(allocations, default=lambda o: o.__dict__ if not isinstance(o, (
            datetime.date, datetime.datetime)) else o.isoformat(), indent=4)))
    else:
        return jsonify(status_code=400)


@app.route(f'{API_V1_ROOT}faculties/', methods=['GET'])
def faculties():
    return jsonify(FACULTY_CHOICES)


@app.route(f'{API_V1_ROOT}building-keys/', methods=['GET'])
def building_keys():
    return jsonify(BUILDING_KEY_CHOICES)


def get_enum(enum, key: str):
    result = [member for name, member in enum.__members__.items() if str(member.name).lower() == key.lower()]
    return result[0] if result else None


if __name__ == '__main__':
    app.run()
