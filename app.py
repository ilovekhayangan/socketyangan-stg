from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, rooms

from publish import handler as publish_handler

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")

users = {}


@app.route("/")
def home():
    return "<h1>Welcome to Khayangan</h1>"


@app.route("/test")
def test():
    socketio.emit("response", {"from": "server", "data": "Ini cuma test bro"})
    return "Success emit test to client"


@app.route("/test/<message>")
def test_msg(msg):
    print("msg: ", msg)
    socketio.emit("response", {"from": "server", "data": msg})
    return "Success emit test to client"


@app.route("/event", methods=["POST"])
def publish_event():
    return publish_handler(request, jsonify, socketio)


@socketio.on("setSocketId")
def set_socket_id(data):
    print(data)
    email = data["email"]
    name = data["name"]
    socket_id = data["socketId"]
    users[email] = socket_id

    # emit to socketId
    emit("response", {"email": email, "name": name}, to=socket_id)


@socketio.on("joinRoom")
def on_join(data):
    print(data)
    room = data["room"]
    join_room(room)
    emit("response", "Joined " + room, room=room)
    # print list of rooms
    print(rooms())


@socketio.on("message")
def message(data):
    print(data)  # {'from': 'client'}
    emit("response", {"from": "server"})


# @socketio.on('request')
# def request(data):
#     print(data)  # {'from': 'client'}


if __name__ == "__main__":
    socketio.run(app)
