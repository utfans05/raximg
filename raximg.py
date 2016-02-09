import requests
import getpass
import readline
import time

# request to authenticate and returns a tuple with token and account number
def get_token(username,password):
    url = "https://identity.api.rackspacecloud.com/v2.0/tokens"
    headers = {'Content-type': 'application/json'}
    payload = {'auth':{'passwordCredentials':{'username': username,'password': password}}}
    r = requests.post(url, headers=headers, json=payload)
    print r.json()


def create_container(token, account, region, container):
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

    create_container(token,account,region,container)

    url = "https://" + region +".images.api.rackspacecloud.com/v2/tasks"
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
    payload = {"type": "export","input":{"image_uuid": img_id,"receiving_swift_container": container}}
    r = requests.post(url, headers=headers, json=payload)
    data = r.json()
    task_id = walk(data,'id')
    print(task_id)
    task_status(region, task_id)

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

def upload_vhd(token, account):
    region = raw_input("Region: ")
    container = raw_input("Container: ")
    vhd = raw_input("File: ")

    create_container(token,account,region,container)

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

    headers = {"X-Auth-Token": token, "Content-Type": "application/octet-stream"}
    with open(vhd, 'rb') as f:
        r = requests.put(url,headers=headers,data=f)

def import_img(token):
    region = raw_input('region: ')
    container = raw_input('container: ')
    vhd = raw_input('image name: ')

    url = "https://" + region +".images.api.rackspacecloud.com/v2/tasks"
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
    payload = {"type": "import","input":{"image_properties": {"name": vhd},"import_from": container + "/" + vhd}}
    r = requests.post(url, headers=headers, json=payload)

def update_img(token):
    region = raw_input('region: ')
    img_id = raw_input('image id: ')

    url = "https://" + region + ".images.api.rackspacecloud.com/v2/images/" + img_id
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token, 'Accept': 'application/openstack-images-v2.1-json-patch'}
    payload = {"op": "add", "path": "/vm-mode", "value": "hvm"}
    r = requests.patch(url,headers=headers, json=payload)
    data = r.json()
    print(data)

def task_status(region, task_id):
    url = "https://" + region +".images.api.rackspacecloud.com/v2/tasks" + "/" + task_id
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
    r = requests.get(url, headers=headers)
    data = r.text
    print(data)
    status = walk(data, 'status')
    print(status)
    while(status != 'success'):
        r = requests.get(url, headers=headers)
        data = r.text
        status = walk(data,'status')
        print(status)
        time.sleep(15)
    print(status)

def menu():
    print("Choose an action: ")
    print("1. export")
    print("2. import")
    print("3. download")
    print("4. upload")
    action = raw_input()

    if action == "1":
        export_img(token)
        menu()
    elif action == "2":
        import_img(token)
        menu()
    elif action == "3":
        download_vhd(token, account)
        menu()
    elif action == "4":
        upload_vhd(token,account)
        menu()
    else:
        print("Try again")
        menu()

# start by asking for credentilas
username = raw_input('username: ')
password = getpass.getpass('password: ')

# grab token and account info
token = get_token(username,password)

# ask the user what to do
#menu()
#update_img(token)
