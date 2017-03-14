import requests


def get_server_status(url):
    try:
        r = requests.head(url)
    except:
        return ServerState.MACHINE_DOWN_STR
    if str(r.status_code).startswith('5'):
        return ServerState.MACHINE_DOWN_STR
    return ServerState.MACHINE_UP_STR


class Server(object):
    def set_port(self, port):
        self.port = port

    def get_port(self):
        return self.port

    def __init__(self, name, url, port):
        if not url.startswith('http'):
            url = 'http://' + url
            url = url.strip('/')
        self.url = url
        self.port = port
        self.name = name
        self.complete_url = self.get_complete_url()
        # servername-port
        self.last_state_filename = name + "-" + str(port)
        self.curr_state = None
        self.prev_state = self.get_last_state()
        self.is_status_changed = False
        self.is_status_changed = False
        self.gunicorn_state = None
        self.machine_state = None
        # down time of server in minutes
        self.down_time = 0
        self.should_send_mail = False

    def get_name(self):
        return self.name

    def get_complete_url(self):
        return self.url.strip('/') + ":" + str(self.port)

    def set_status(self, status):
        # if machine is down or gunicorn is not running change curr_status to down
        if status == ServerState.MACHINE_DOWN or status == ServerState.GUNICORN_STOPPED or status == \
                ServerState.MACHINE_DOWN_STR:
            self.curr_state = ServerState.MACHINE_DOWN_STR
        else:
            self.curr_state = ServerState.MACHINE_UP_STR

        # write the status to file
        self.save_last_state_to_file()
        # book keeping of other server state
        self.server_bookkeeping(status)

        if self.down_time == ServerState.DOWN_TIME_THRESHOULD:
            self.should_send_mail = True
            # if server down time is greater than DOWN_TIME_THRESHOLD and currently server is brought up then send mail
        elif self.curr_state == ServerState.MACHINE_UP_STR and self.down_time >= ServerState.DOWN_TIME_THRESHOULD:
            self.should_send_mail = True
        else:
            self.should_send_mail = False

        if self.curr_state == ServerState.MACHINE_DOWN_STR:
            self.down_time += 1
        else:
            self.down_time = 0

        if self.prev_state != self.curr_state:
            self.is_status_changed = True
        else:
            self.is_status_changed = False

        self.prev_state = self.curr_state

    def server_bookkeeping(self, status):
        if status == ServerState.MACHINE_DOWN or status == ServerState.MACHINE_DOWN_STR:
            self.machine_state = 0
            self.gunicorn_state = 0
        if status == ServerState.GUNICORN_RUNNING:
            self.machine_state = 1
            self.gunicorn_state = 1
        if status == ServerState.GUNICORN_STOPPED:
            self.machine_state = 1
            self.gunicorn_state = 0

    def get_status(self):
        return self.curr_state

    def is_status_changed(self):
        return self.is_status_changed

    def is_down(self):
        return self.curr_state == ServerState.MACHINE_DOWN_STR

    def get_last_state(self):
        try:
            f = open(self.last_state_filename, "r")
            last_state = f.read()
            # if running this script for first time there will be no last state files
            # so ping the server get the status and write
            # it to the file
            # if empty file is present
            if len(last_state) == 0:
                self.curr_state = get_server_status(self.complete_url)
            f.close()
        except:
            # if no file is there
            # print("{0} file not found creating".format(self.last_state_filename))
            last_state = get_server_status(self.complete_url)
        return last_state

    def save_last_state_to_file(self):
        try:
            f = open(self.last_state_filename, "w")
            f.write(self.curr_state)
            f.close()
        except:
            print('file writing error')
            exit(0)

    def ping(self):
        try:
            r = requests.head(self.complete_url)
        except:
            # server is down
            self.set_status(ServerState.MACHINE_DOWN)
            return
        status_code = str(r.status_code)
        # print(status_code)
        if status_code.startswith('5'):
            self.set_status(ServerState.GUNICORN_STOPPED)
        else:
            self.set_status(ServerState.GUNICORN_RUNNING)

    def __str__(self):
        return "name:{0}\nurl:{1}\nport:{2}\nprev_status:{3}\ncurr_status:{4}\nis_status_changed:{5}\n is_down:{" \
               "6}".format(
            self.name, self.url, self.port, self.prev_state, self.curr_state, self.is_status_changed, self.is_down())


class ServerState:
    MACHINE_UP_STR = 'up'
    MACHINE_DOWN_STR = 'down'
    MACHINE_DOWN = -1
    GUNICORN_STOPPED = -2
    MACHINE_UP = 1
    GUNICORN_RUNNING = 2
    # 15 minutes down time for server after that send mail
    DOWN_TIME_THRESHOULD = 10

# test_server = Server('localhost', 'localhost', 8000)
# test_server.ping()
# print(test_server.get_status())
# print("ischanged : {0}".format(test_server.is_status_changed))
