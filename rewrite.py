import requests

def walk(obj, key):
    stack = obj.items()
    while stack:
        k, v = stack.pop()
        if isinstance(v, dict):
            stack.extend(v.iteritems())
        else:
            if k == key:
                if len(v) == 6:
                    account = v
                        if len(v) == 142:
                            return v
                        #print("%s: %s" % (k,v))

def get_token(username,passwd):
    url = "https://identity.api.rackspacecloud.com/v2.0/tokens"
    headers = {'Content-type': 'application/json'}
    payload = {'auth':{'passwordCredentials':{'username': username,'password': password}}}
    r = requests.post(url, headers=headers, json=payload)
    data = r.json()
    token = walk(data, 'id')
    return token

def export_img(token):
    region = raw_input('region: ')
    container = raw_input('container: ')
    img_id = raw_input('image id: ')

    url = "https://" + region +".images.api.rackspacecloud.com/v2/tasks"
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
    payload = {"type": "export","input":{"image_uuid": img_id,"receiving_swift_container": container}}
    r = requests.post(url, headers=headers, json=payload)
    data = r.json()
    print(data)

def task_status():


username = raw_input('username: ')
password = raw_input('password: ')

token = get_token(username,password)
export_img(token)
