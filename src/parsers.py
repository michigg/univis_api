from typing import List

from flask_restplus import reqparse, inputs

lectures_parser = reqparse.RequestParser()
lectures_parser.add_argument('search_token', required=True,
                             type=str,
                             help='part of a lecture name')

rooms_parser = reqparse.RequestParser()
rooms_parser.add_argument('search_token',
                          type=str,
                          help='part of a room short name (e.g. WE5/01.006)')
rooms_parser.add_argument('name',
                          type=str,
                          help='rooms short name (e.g. WE5/01.006)')
rooms_parser.add_argument('long_name',
                          type=str,
                          help='rooms name (e.g. Seminarraum)')
rooms_parser.add_argument('size',
                          type=int,
                          help='rooms size')
rooms_parser.add_argument('faculty',
                          type=str,
                          help='rooms faculty univis name')
rooms_parser.add_argument('building_keys',
                          type=List[str],
                          help='rooms filtered by list of building_keys')

allocations_parser = reqparse.RequestParser()
allocations_parser.add_argument('start_date', type=inputs.regex('^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$'),
                                help='date from which allocations are to be searched for (format:  %Y-%m-%d)')
allocations_parser.add_argument('end_date', type=inputs.regex('^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$'),
                                help='date to which allocations are to be searched for (format:  %Y-%m-%d)')
allocations_parser.add_argument('start_time', type=inputs.regex('^(?:[01]\d|2[0123]):(?:[012345]\d)$'),
                                help='time from which allocations are to be searched for (format:  %H:%M)')
allocations_parser.add_argument('end_time', type=inputs.regex('^(?:[01]\d|2[0123]):(?:[012345]\d)$'),
                                help='time to which allocations are to be searched for (format:  %H:%M)')
