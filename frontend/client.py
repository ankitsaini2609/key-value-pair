import websocket
try:
    import thread
except ImportError:
    import _thread as thread
from colorama import Fore, init
import time
import json


init(autoreset=True)  # To reset the terminal color
action_keys_value = {'1': 'get', '2': 'put', '3': 'delete', '4': 'watch', '5': 'show_all', '6': 'exit'}

def get_value(key):
    """
    It is mapping the key and action
    :param key: key number
    :return: name of the action
    """
    global action_keys_value
    return action_keys_value[key]

def get_data(action_code):
    """
    on the basis of action it will choose the option.
    :param action:
    :return:
    """
    action = get_value(action_code)
    if action == "get":
        print("Enter the key for which you want to access data: ")
        data = input().strip()
    elif action == "put":
        print("Enter data, key-value and watch separated by comma:")
        data = input().strip()
    elif action == "delete":
        print("Enter the key for which you want to delete data: ")
        data = input().strip()
    elif action == "watch":
        print("Enter the key for which you want to watch: ")
        data = input().strip()
    elif action == "exit":
        data = ""
    else:
        data = ""
    return data


def main(ws):
    """
    It will take input from the client and process it.
    :param ws: class object
    :return:
    """
    while True:
        try:
            print("Enter Choice: ")
            action_code = input()
            data = get_data(action_code)
            message = {"action": action_code, "data": data}
            #print(message)
            ws.send(json.dumps(message))
        except Exception as err:
            print(err)


def on_message(ws, message):
    """
    callable object which is called when received data.
    on_message has 2 arguments.
    :param ws: class object
    :param message: is utf-8 string which we get from the server.
    :return:
    """
    print(Fore.GREEN + "one new message received from server")
    recv_msg = json.loads(message)
    if recv_msg['status'] == 0:
        print(Fore.RED + recv_msg['message'])
    else:
        print(Fore.GREEN + recv_msg['message'])
        print("Enter choice: ")

def on_error(ws, error):
    """
     callable object which is called when we get error.
     on_error has 2 argument:
     :param ws: class object
     :param error: exception object
    """
    print(error)

def on_close(ws):
    """
    callable object which is called when closed the connection.
    on_close has one argument.
    :param ws: class object
    :return:
    """
    print("### closed ###")

def on_open(ws):
    """callable object which is called at opening websocket.
       this function has one argument.
       :param ws: class object
       :return:
    """
    def run(*args):
        main(ws)
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    try:
        ws = websocket.WebSocketApp("ws://172.17.0.1/ws"
                                    , on_message=on_message
                                    , on_error=on_error
                                    , on_close=on_close)
        ws.on_open = on_open
        ws.run_forever()
    except Exception as err:
        print(Fore.RED + err)
        print("Waiting for server")
        time.sleep(10)