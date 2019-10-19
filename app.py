import datetime
import json

from flask import Flask, request, jsonify

from utils.allocation_controller import UnivISAllocationController
from utils.controllers import UnivISLectureController, UnivISRoomController

API_V1_ROOT = "/api/v1/"
app = Flask(__name__)


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
def rooms():
    search_token = request.args.get('token', None)
    if search_token:
        univis_room_c = UnivISRoomController()
        rooms = sorted(univis_room_c.get_tokens_rooms(token=search_token), key=lambda room: room.__str__())
        room_dicts = [room.__dict__ for room in rooms]
        return jsonify(room_dicts)
    else:
        return jsonify(status_code=400)


@app.route(f'{API_V1_ROOT}allocations/', methods=['GET'])
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


if __name__ == '__main__':
    app.run()
