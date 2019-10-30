from typing import List

from flask_restplus import reqparse, inputs

lectures_parser = reqparse.RequestParser()
lectures_parser.add_argument('search_token',
                             type=str,
                             help='part of a lecture name')
lectures_parser.add_argument('department',
                             type=str,
                             help='filter lectures by Name or UnivIS-org-number of the lectures department')
lectures_parser.add_argument('chapter',
                             type=str,
                             help='filter lectures by the name of the lectures headline in the lecture directory')
lectures_parser.add_argument('name',
                             type=str,
                             help='filter lectures by the long name of a lecture')
lectures_parser.add_argument('short_name',
                             type=str,
                             help='filter lectures by the short name of a lecture')
lectures_parser.add_argument('type',
                             type=str,
                             help='filter lectures by lecture type (like shorthand in the lecture directory)')
lectures_parser.add_argument('number',
                             type=int,
                             help='filter lectures by the Document number of the business event (if available)')
lectures_parser.add_argument('sws',
                             type=int,
                             help='filter lectures by semester hours per week')
lectures_parser.add_argument('bonus_points',
                             type=int,
                             help='filter lectures by the amount of bonus points (equals)')
lectures_parser.add_argument('malus_points',
                             type=int,
                             help='filter lectures by the amount of malus points (equals)')
lectures_parser.add_argument('ects_credits',
                             type=float,
                             help='filter lectures by the amount of ects (equals)')
lectures_parser.add_argument('lecturer',
                             type=str,
                             help='filter lectures by the lecturers name')
lectures_parser.add_argument('room_short',
                             type=str,
                             help='filter lectures by the rooms short name')
lectures_parser.add_argument('path',
                             type=str,
                             help='part of a lecture name')
lectures_parser.add_argument('token',
                             type=str,
                             help='?')
lectures_parser.add_argument('token_reg',
                             type=str,
                             help='?')
lectures_parser.add_argument('token_attr',
                             type=str,
                             help='?')
lectures_parser.add_argument('token_sem',
                             type=str,
                             help='?')
lectures_parser.add_argument('evaluation',
                             type=str,
                             help='?')
lectures_parser.add_argument('allocation',
                             type=str,
                             help='?')
lectures_parser.add_argument('no_imports',
                             type=bool,
                             help='if true: show no imported lectures')
lectures_parser.add_argument('no_subchap',
                             type=bool,
                             help='if true: show no lectures which titles are sub titles of the request')
lectures_parser.add_argument('no_titles',
                             type=bool,
                             help='if true: show no lecture titles')

rooms_parser = reqparse.RequestParser()
rooms_parser.add_argument('token',
                          type=str,
                          help='part of a room short name (e.g. WE5/01.006)'
                          )
rooms_parser.add_argument('name',
                          type=str,
                          help='rooms short name (e.g. WE5/01.006)'),
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
                          type=list,
                          action='append',
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

persons_parser = reqparse.RequestParser()
persons_parser.add_argument('token',
                            type=str,
                            help='part of a full name'
                            )
persons_parser.add_argument('full_name',
                            type=str,
                            help='the persons full name', )
persons_parser.add_argument('first_name',
                            type=str,
                            help='the persons name')
persons_parser.add_argument('last_name',
                            type=str,
                            help='the persons last name')
persons_parser.add_argument('title',
                            type=str,
                            help='the persons title')
