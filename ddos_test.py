
import requests
import threading
import time

l = [];  

def current_milli_time():
    return round(time.time()*1000)

def current_sec_time():
    return round(time.time())


def countRequestPerMinute(timeTook):
    t = current_sec_time()

    l.append({
        "time_took": timeTook,
        "time_received": t
    })

    for e in l:
        if current_sec_time() -e["time_received"] >= 60:
            l.remove(e)

def make_request(name):
    while True:
        s = current_milli_time()
        r = requests.get('http://127.0.0.1:24899')
        t = current_milli_time() - s
        print("Response code: {} Took {} ms".format(str(r.status_code),t), end="")
        countRequestPerMinute(t)

thread = 128
i = 0
while i <= thread:
# while True:
    x = threading.Thread(target=make_request,args=(i,))
    # print("Starting thread {}".format(i))
    x.start()
    i+=1


    print("Initial Start Please Wait..")
    time.sleep(5)
    while len(l) > 0:
        time.sleep(1)
        response_time = 0
        for e in l:
            response_time = response_time + e['time_took']
        response_time = response_time / len(l)

        # print("Request per second: {}".format(len(l)))
        # print("Average Response time: {} Ms".format(round(response_time)))
        
        #print("\rAverage response time: {} Ms and Request per/sec: {}".format(round(response_time),len(l)), end=""),