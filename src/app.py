import datetime
import json
from pprint import pprint

from flask import Flask, request, jsonify
from flask_caching import Cache
from flask_restplus import Api, Resource

import parsers
from config import PROD_MODE, CACHE_REDIS_URL, API_V1_ROOT
from controllers.allocation_controller import UnivISAllocationController
from controllers.controllers import UnivISLectureController
from controllers.person_controller import UnivISPersonController
from controllers.room_controller import UnivISRoomController
from models.enums.building_key import CHOICES as BUILDING_KEY_CHOICES
from models.enums.faculty import CHOICES as FACULTY_CHOICES

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
        args = {"id": id}

        univis_room_c = UnivISRoomController()
        url = univis_room_c.get_url(args=args)
        rooms = univis_room_c.get_univis_data_rooms([url])
        return jsonify(rooms[0].__dict__) if rooms else jsonify(status_code=400)


@api.route(f'{API_V1_ROOT}rooms/')
class Rooms(Resource):

    @cache.cached(timeout=86400, key_prefix=make_cache_key)
    @api.doc(parser=parsers.rooms_parser)
    def get(self):
        """
        returns univis rooms
        """
        args = parsers.rooms_parser.parse_args()

        univis_room_c = UnivISRoomController()
        urls = univis_room_c.get_all_rooms_urls() if self.is_param_list_empty(args) else [
            univis_room_c.get_url(args=args)]
        rooms = univis_room_c.get_univis_data_rooms(urls=urls)
        return json.loads(json.dumps(rooms, default=lambda o: o.__dict__ if not isinstance(o, (
            datetime.date, datetime.datetime)) else o.isoformat(), indent=4))

    def is_param_list_empty(self, args):
        empty_params = True
        for key in args:
            if args[key]:
                empty_params = False
        return empty_params


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


@api.route(f'{API_V1_ROOT}persons/')
class Persons(Resource):

    @cache.cached(timeout=86400, key_prefix=make_cache_key)
    @api.doc(parser=parsers.persons_parser)
    def get(self):
        """
        returns univis rooms
        """
        args = parsers.persons_parser.parse_args()

        univis_person_c = UnivISPersonController()
        urls = None if self.is_param_list_empty(args) else [univis_person_c.get_url(args=args)]

        if urls:
            persons = univis_person_c.get_univis_data_persons(urls=urls)
            return json.loads(json.dumps(persons, default=lambda o: o.__dict__ if not isinstance(o, (
                datetime.date, datetime.datetime)) else o.isoformat(), indent=4))
        else:
            return jsonify(status_code=400)

    def is_param_list_empty(self, args):
        empty_params = True
        for key in args:
            if args[key]:
                empty_params = False
        return empty_params


@api.route(f'{API_V1_ROOT}persons/<int:id>')
class Person(Resource):
    def get(self, id):
        """
        returns room by id (beta)
        """
        args = {"id": id}

        univis_person_c = UnivISPersonController()
        url = univis_person_c.get_url(args=args)
        univis_persons = univis_person_c.get_univis_data_persons([url])
        if univis_persons:
            return json.loads(json.dumps(univis_persons[0], default=lambda o: o.__dict__ if not isinstance(o, (
                datetime.date, datetime.datetime)) else o.isoformat(), indent=4))
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


if __name__ == '__main__':
    app.run()
