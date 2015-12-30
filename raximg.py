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
                elif len(v) == 142:
                    return v, account
                    #print("%s: %s" % (k,v))

def get_token(username,passwd):
    url = "https://identity.api.rackspacecloud.com/v2.0/tokens"
    headers = {'Content-type': 'application/json'}
    payload = {'auth':{'passwordCredentials':{'username': username,'password': password}}}
    r = requests.post(url, headers=headers, json=payload)
    data = r.json()
    token = walk(data, 'id')
    return token

def create_container(token, account):
    region = raw_input("Region: ")
    container = raw_input("Container: ")

    if region == "dfw":
        url = "https://storage101.dfw1.clouddrive.com/v1/MossoCloudFS_" + account + "/" + container
    elif region == "iad":
        url = "https://storage101.iad3.clouddrive.com/v1/MossoCloudFS_" + account + "/" + container
    elif region == "ord":
        url = "https://storage101.ord1.clouddrive.com/v1/MossoCloudFS_" + account + "/" + container
    elif region == "syd":
        url = "https://storage101.syd2.clouddrive.com/v1/MossoCloudFS_" + account + "/" + container
    elif region == "hkg":
        url = "https://storage101.hkg1.clouddrive.com/v1/MossoCloudFS_" + account + "/" + container

    headers = {"X-Auth-Token": token}
    r = requests.put(url, headers=headers)

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

def download_vhd(token, account):
    region = raw_input("Region: ")
    container = raw_input("Container: ")
    vhd = raw_input("File: ")

    if region == "dfw":
        url = "https://storage101.dfw1.clouddrive.com/v1/MossoCloudFS_" + account + "/" + container + "/" + vhd
    elif region == "iad":
        url = "https://storage101.iad3.clouddrive.com/v1/MossoCloudFS_" + account + "/" + container + "/" + vhd
    elif region == "ord":
        url = "https://storage101.ord1.clouddrive.com/v1/MossoCloudFS_" + account + "/" + container + "/" + vhd
    elif region == "syd":
        url = "https://storage101.syd2.clouddrive.com/v1/MossoCloudFS_" + account + "/" + container + "/" + vhd
    elif region == "hkg":
        url = "https://storage101.hkg1.clouddrive.com/v1/MossoCloudFS_" + account + "/" + container + "/" + vhd

    headers = {"X-Auth-Token": token}
    r = requests.get(url,headers=headers, stream=True)
    with open(vhd, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return vhd

username = raw_input('username: ')
password = raw_input('password: ')

token, account = get_token(username,password)
#create_container(token, account)
#export_img(token)
download_vhd(token, account)
