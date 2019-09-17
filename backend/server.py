#!/usr/bin/python3.5

from gevent import pywsgi
from flask import Flask
import json
from colorama import Fore, init
from flask_sockets import Sockets
from geventwebsocket.handler import WebSocketHandler

users = []
user_data = {}
clients = []
watch_list = []
action_keys_value = {'1': 'get', '2': 'put', '3': 'delete', '4': 'watch', '5': 'show_all', '6': 'exit'}

init(autoreset=True)  # To reset the terminal color
app = Flask(__name__)
sockets = Sockets(app)

welcome_message = Fore.GREEN + """
                Welcome to key value pair store (use ',' as separator between key, value and watch(0/1)(yes/no))
                Choose your option:
                1 - Get the key value pair 
                2 - Put the key value pair 
                3 - Delete key value pair 
                4 - watch the key         
                5 - show all
                6 - exit

"""


def get_value(key):
    """
    It is mapping the key and action
    :param key: key number
    :return: name of the action
    """
    global action_keys_value
    return action_keys_value[key]


def alert_user(key):
    """
    It will send the alert to the user.
    :param key: they key which is changed and added to user watchlist
    :return:
    """
    global users
    for user in users:
        if key in user.watchlist:
            try:
                user.socket.send(
                    json.dumps({'status': 1, 'message': key + ' has been updated to ' + str(user_data[key])}))
            except Exception as err:
                users.remove(user)


def process_request(user, message):
    """
    It will process the request of the user.
    :param user: user details
    :param message: what user is requesting
    :return: response according to user request
    """
    global user_data
    global watch_list
    response_message = {'message': 'Successful', 'status': 1}
    action = get_value(message['action'])
    if action == 'get':
        response_message['message'] = str(user_data.get(message['data'], None))
    elif action == 'put':
        try:
            key, value, watch = message['data'].split(",")
            user_data[key] = value
            if key in watch_list:
                alert_user(key)
            elif watch:
                watch_list.append(key)
                user.watchlist.append(key)
        except Exception as err:
            response_message['status'] = 0
            response_message['message'] = err.__str__()
    elif action == 'delete':
        try:
            del user_data[message['data']]
        except Exception as err:
            response_message['status'] = 0
            response_message['message'] = err.__str__()
    elif action == 'watch':
        if message['data'] not in user.watchlist:
            user.watchlist.append(message['data'])
    elif action == 'show_all':
        response_message['message'] = json.dumps(user_data)

    return json.dumps(response_message)


class User:
    """
    This is the user class which will save the socket and create watch list for each user
    """

    def __init__(self, socket):
        """
        :type socket: object
        """
        self.socket = socket
        self.watchlist = list()


@sockets.route('/ws')
def join(socket):
    """
    It will receive a socket and maintain the connection
    :param socket: socket for which we need to maintain the connection
    :return:
    """
    global users
    global user_data
    user = User(socket)  # To save the the socket and add it to watch_list
    users.append(user)
    socket.send(json.dumps({"message": welcome_message, "status": 1}))
    while not socket.closed:
        try:
            recv_request = socket.receive()
            message = json.loads(recv_request)
            print("user_data:" + str(user_data))
            action = get_value(message['action'])
            if action == 'exit':
                break
            recv_response = process_request(user, message)
            socket.send(recv_response)
        except Exception as err:
            print(err)
            break
    users.remove(user)


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0', 80), app, handler_class=WebSocketHandler)
    server.serve_forever()