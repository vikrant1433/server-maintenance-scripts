import datetime
from time import sleep

from send_email2 import send_email
from server import Server


def make_subject(server):
    return server.get_name() +' on port {0}'.format(server.port) + ' is {0}'.format(server.get_status())


def make_body(server):
    if server.machine_state == 0:
        return server.get_complete_url() + " machine was down from last 15 minutes"
    if server.gunicorn_state == 0:
        return server.get_complete_url() + " machine is up but gunicorn is not running :("
    return "{0} is now up and running :)".format(server.get_complete_url())


def send_notification(server):
    to = ['vikrant@cse.iitb.ac.in']
    # cc = []
    if server.get_name().startswith("bodhitree"):
        cc = ['br@cse.iitb.ac.in', 'swaresh@cse.iitb.ac.in', 'anjalikj@cse.iitb.ac.in', 'akashkumar@cse.iitb.ac.in',
              'chebrolu@cse.iitb.ac.in','m.sonika30@gmail.com']
    else:
        cc = ['br@cse.iitb.ac.in']
    sub = make_subject(server)
    body = make_body(server)
    send_email(to=to, cc=cc, subject=sub, body=body)


bt1_80 = Server(name='bodhitree1', port=80, url='http://bodhitree1.cse.iitb.ac.in')
#  bt3_8888 = Server(name='bodhitree3', port=8888, url='http://bodhitree3.cse.iitb.ac.in')
#  bt3_80 = Server(name='bodhitree3', port=9090, url='http://bodhitree3.cse.iitb.ac.in')
bt3_80 = Server(name='bodhitree3', port=80, url='http://bodhitree3.cse.iitb.ac.in')
safestreet = Server(name='safestreet', port=80, url='http://safestreet.cse.iitb.ac.in')
# test_server = Server(name='vikrant', port=8000, url='http://localhost')

server_list = [bt1_80, bt3_80, safestreet]
#  server_list = [safestreet]
# server_list = [test_server]
while True:
    # sleep for 60 second
    sleep(60)
    for server in server_list:
        server.ping()
        print("{0} | {1} |{2}".format(datetime.datetime.now(), server.get_complete_url(), server.get_status()))
        if server.should_send_mail:
            send_notification(server)
