import requests
import getpass
import readline
import time
import json
import argparse
import logging
logging.captureWarnings(True)

parser = argparse.ArgumentParser()
parser.add_argument("action", help="Actions include: import,export,download, status, upload or update")
parser.add_argument("-u", "--username", help="Rackspace cloud account username.")
parser.add_argument("-p", "--password", help="Rackspace cloud account password.")
parser.add_argument("-i", "--image", help="Image to use for action.")
parser.add_argument("-c", "--container", help="Container to use for action.")
parser.add_argument("-r", "--region", help="Region of the image.")
args = parser.parse_args()

# request to authenticate and returns a tuple with token and account number
def get_token(username,password):
    url = "https://identity.api.rackspacecloud.com/v2.0/tokens"
    headers = {'Content-type': 'application/json'}
    payload = {'auth':{'passwordCredentials':{'username': username,'password': password}}}
    r = requests.post(url, headers=headers, json=payload)
    data = r.json()
    token = (data["access"]["token"]["id"])
    account = (data["access"]["token"]["tenant"]["id"])
    return token,account

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

def export_img(token,account,region,container,image):
    create_container(token,account,region,container)

    url = "https://" + region +".images.api.rackspacecloud.com/v2/tasks"
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
    payload = {"type": "export","input":{"image_uuid": image,"receiving_swift_container": container}}
    r = requests.post(url, headers=headers, json=payload)
    data = r.json()
    task_id = data["id"]
    task_status(token,region,task_id)

def download_img(token, account, region, image, container):
    if region == "dfw":
        url = "https://storage101.dfw1.clouddrive.com/v1/MossoCloudFS_" + account + "/" + container + "/" + image
    elif region == "iad":
        url = "https://storage101.iad3.clouddrive.com/v1/MossoCloudFS_" + account + "/" + container + "/" + image
    elif region == "ord":
        url = "https://storage101.ord1.clouddrive.com/v1/MossoCloudFS_" + account + "/" + container + "/" + image
    elif region == "syd":
        url = "https://storage101.syd2.clouddrive.com/v1/MossoCloudFS_" + account + "/" + container + "/" + image
    elif region == "hkg":
        url = "https://storage101.hkg1.clouddrive.com/v1/MossoCloudFS_" + account + "/" + container + "/" + image

    headers = {"X-Auth-Token": token}
    r = requests.get(url,headers=headers, stream=True)
    with open(image, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return image

def upload_img(token, account,region, container, image):
    create_container(token,account,region,container)

    if region == "dfw":
        url = "https://storage101.dfw1.clouddrive.com/v1/MossoCloudFS_" + account + "/" + container + "/" + image
    elif region == "iad":
        url = "https://storage101.iad3.clouddrive.com/v1/MossoCloudFS_" + account + "/" + container + "/" + image
    elif region == "ord":
        url = "https://storage101.ord1.clouddrive.com/v1/MossoCloudFS_" + account + "/" + container + "/" + image
    elif region == "syd":
        url = "https://storage101.syd2.clouddrive.com/v1/MossoCloudFS_" + account + "/" + container + "/" + image
    elif region == "hkg":
        url = "https://storage101.hkg1.clouddrive.com/v1/MossoCloudFS_" + account + "/" + container + "/" + image

    headers = {"X-Auth-Token": token, "Content-Type": "application/octet-stream"}
    with open(image, 'rb') as f:
        r = requests.put(url,headers=headers,data=f)

def import_img(token, image, container):
    url = "https://" + region +".images.api.rackspacecloud.com/v2/tasks"
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
    payload = {"type": "import","input":{"image_properties": {"name": image},"import_from": container + "/" + image}}
    r = requests.post(url, headers=headers, json=payload)

    data = r.json()
    task_id = data["id"]
    task_status(token,region,task_id)

def update_img(token,region,image):
    url = "https://" + region + ".images.api.rackspacecloud.com/v2/images/" + imgage
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token, 'Accept': 'application/openstack-images-v2.1-json-patch'}
    payload = {"op": "add", "path": "/vm-mode", "value": "hvm"}
    r = requests.patch(url,headers=headers, json=payload)
    data = r.json()
    print(data)

def task_status(token, region, task_id):
    url = "https://" + region +".images.api.rackspacecloud.com/v2/tasks" + "/" + task_id
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
    r = requests.get(url, headers=headers)
    data = r.json()
    status = data["status"]
    print(status)
    while(status != 'success'):
        r = requests.get(url, headers=headers)
        data = r.json()
        status = data["status"]
        print(status)
        time.sleep(15)
    if status == 'failure':
        print("Something went wrong.")
    print(status)

token,account = get_token(args.username,args.password)

if args.action == "export":
    export_img(token, account, args.region,args.container, args.image)
elif args.action == "import":
    import_img(token, args.image, args.container)
elif args.action == "download":
    download_img(token, account, args.region, args.image, args.container)
elif args.action == "upload":
    upload_img(token, account, args.region, args.container, args.image)
else:
    print("bad input")
