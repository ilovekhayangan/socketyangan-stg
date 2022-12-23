import json
import os

import requests

VERIFY_TOKEN_URL = os.environ.get("VERIFY_TOKEN_URL")


def handler(request, jsonify, socketio):
    # Get the request body
    body = request.get_json()
    print("body:", body)

    try:
        user_email = body["email"]
    except:  # pylint: disable=bare-except
        return jsonify({"message": "Email is required"}), 422

    try:
        event = body["event"]
    except:  # pylint: disable=bare-except
        return jsonify({"message": "Event is required"}), 422

    try:
        event_data = body["event-data"]
    except:  # pylint: disable=bare-except
        return jsonify({"message": "Event-data is required"}), 422

    try:
        socketio.emit(event, json.dumps(event_data), room=user_email)

        result = {
            "message": "Success",
            "to": {
                "email": user_email,
            },
            "event": event,
            "event-data": json.dumps(event_data),
        }

        return jsonify(result), 200
    except Exception as err:  # pylint: disable=bare-except # pylint: disable=broad-except
        return jsonify({"message": "Error: " + str(err)}), 500
