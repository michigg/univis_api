import datetime
import json

from flask import Flask, request, jsonify
from flask_caching import Cache
from flask_restplus import Api, Resource

import parsers
from config import PROD_MODE, CACHE_REDIS_URL, API_V1_ROOT
from models.enums.building_key import CHOICES as BUILDING_KEY_CHOICES, BuildingKey
from models.enums.faculty import CHOICES as FACULTY_CHOICES, Faculty
from utils.allocation_controller import UnivISAllocationController
from utils.controllers import UnivISLectureController
from utils.room_controller import UnivISRoomController

app = Flask(__name__)
api = Api(app=app, doc='/docs', version='1.0', title='Alternative UnivIS API',
          description='Alternative Universitäres Informationssystem API')

if PROD_MODE:
    cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': CACHE_REDIS_URL})
else:
    cache = Cache(app, config={'CACHE_TYPE': 'simple'})


def make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    return (path + args)


@api.route(f'{API_V1_ROOT}lectures/')
class Lectures(Resource):

    @api.doc(parser=parsers.lectures_parser)
    def get(self):
        """
        returns filtered univis lectures
        """
        search_token = request.args.get('token', None)
        if search_token:
            univis_lecture_c = UnivISLectureController()
            lectures = univis_lecture_c.get_lectures_by_token(search_token)
            if lectures:
                return jsonify(json.dumps(lectures, default=lambda o: o.__dict__ if not isinstance(o, (
                    datetime.date, datetime.datetime)) else o.isoformat(), indent=4))
            return jsonify(status_code=204)
        return jsonify(status_code=400)


@api.route(f'{API_V1_ROOT}rooms/<int:id>')
class Room(Resource):
    def get(self, id):
        """
        returns room by id (beta)
        """
        univis_room_c = UnivISRoomController()
        room = univis_room_c.get_room(id=id)
        return jsonify(room.__dict__) if room else jsonify(status_code=400)


@api.route(f'{API_V1_ROOT}rooms/')
class Rooms(Resource):

    @cache.cached(timeout=86400, key_prefix=make_cache_key)
    @api.doc(parser=parsers.rooms_parser)
    def get(self):
        """
        returns univis rooms
        """
        search_token = request.args.get('token', None)
        name = request.args.get('name', None)
        long_name = request.args.get('long_name', None)
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
            if building_key_enums:
                for building_key_enum in building_key_enums:
                    url = univis_room_c.get_univis_api_url(search_token, name, long_name, size, id, faculty_enum,
                                                           building_key_enum)
                    rooms.extend(univis_room_c.get_rooms(url))
            else:
                url = univis_room_c.get_univis_api_url(search_token, name, long_name, size, id, faculty_enum,
                                                       None)
                rooms.extend(univis_room_c.get_rooms(url))
        else:
            rooms = univis_room_c.get_rooms()
        room_dicts = [room.__dict__ for room in rooms]
        return jsonify(room_dicts)


@api.route(f'{API_V1_ROOT}allocations/')
class Allocations(Resource):

    @cache.cached(timeout=86400, key_prefix=make_cache_key)
    @api.doc(parser=parsers.allocations_parser)
    def get(self):
        """
        returns filtered univis allocations (requires at least one param)
        """
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


@api.route(f'{API_V1_ROOT}faculties/')
class Faculties(Resource):
    def get(self):
        """
        returns current supported faculties
        """
        return jsonify(FACULTY_CHOICES)


@api.route(f'{API_V1_ROOT}building-keys/')
class BuildingKeys(Resource):
    def get(self):
        """
        returns current supported building keys
        """
        return jsonify(BUILDING_KEY_CHOICES)


def get_enum(enum, key: str):
    result = [member for name, member in enum.__members__.items() if str(member.name).lower() == key.lower()]
    return result[0] if result else None


if __name__ == '__main__':
    app.run()
