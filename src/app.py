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
        urls = univis_room_c.get_urls(args=args)
        univis_data = univis_room_c.get_data(urls=urls)
        rooms = univis_room_c.get_rooms(univis_data=univis_data)
        if rooms:
            return json.loads(json.dumps(rooms[0], default=lambda o: o.__dict__ if not isinstance(o, (
                datetime.date, datetime.datetime)) else o.isoformat(), indent=4))
        else:
            return jsonify(status_code=400)


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
        if self.is_param_list_empty(args):
            urls = univis_room_c.get_all_rooms_urls()
        else:
            urls = univis_room_c.get_urls(args=args)
        univis_data = univis_room_c.get_data(urls=urls)
        rooms = univis_room_c.get_rooms(univis_data=univis_data)
        rooms = list(set(rooms))
        if rooms:
            return json.loads(json.dumps(rooms, default=lambda o: o.__dict__ if not isinstance(o, (
                datetime.date, datetime.datetime)) else o.isoformat(), indent=4))
        else:
            return jsonify(status_code=400)

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
        args = parsers.allocations_parser.parse_args()

        univis_allocation_c = UnivISAllocationController()
        if not self.is_param_list_empty(args):
            urls = univis_allocation_c.get_urls(args=args)
            univis_data = univis_allocation_c.get_data(urls=urls)
            allocations = univis_allocation_c.get_allocations(univis_data=univis_data)
            if allocations:
                return json.loads(json.dumps(allocations, default=lambda o: o.__dict__ if not isinstance(o, (
                    datetime.date, datetime.datetime)) else o.isoformat(), indent=4))
        return jsonify(status_code=400)

    def is_param_list_empty(self, args):
        empty_params = True
        for key in args:
            if args[key]:
                empty_params = False
        return empty_params


@api.route(f'{API_V1_ROOT}persons/')
class Persons(Resource):

    @cache.cached(timeout=86400, key_prefix=make_cache_key)
    @api.doc(parser=parsers.persons_parser)
    def get(self):
        """
        returns filtered univis persons
        """
        args = parsers.persons_parser.parse_args()

        univis_person_c = UnivISPersonController()
        if not self.is_param_list_empty(args):
            urls = univis_person_c.get_urls(args=args)
            univis_data = univis_person_c.get_data(urls=urls)
            persons = univis_person_c.get_persons(univis_data=univis_data)
            persons = list(set(persons))
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
        returns person by id (beta)
        """
        args = {"id": id}

        univis_person_c = UnivISPersonController()
        urls = univis_person_c.get_urls(args=args)
        univis_data = univis_person_c.get_data(urls=urls)
        persons = univis_person_c.get_persons(univis_data=univis_data)

        if persons:
            return json.loads(json.dumps(persons[0], default=lambda o: o.__dict__ if not isinstance(o, (
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
