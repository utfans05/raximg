import requests
import time
import json
import argparse
import logging
import sys
from clint.textui import progress
logging.captureWarnings(True)

# Request to authenticate and returns a tuple with token and account number
def get_token(username,password):
    url = "https://identity.api.rackspacecloud.com/v2.0/tokens"
    headers = {'Content-type': 'application/json'}
    payload = {'auth':{'passwordCredentials':{'username': username,'password': password}}}

    try:
        r = requests.post(url, headers=headers, json=payload)
    except requests.ConnectionError as e:
        print("Connection Error: Check your interwebs!")
        sys.exit()

    if r.status_code == 200:
        print("OK. Operation completed successfully.")
    elif r.status_code == 400:
        print("Bad Request. Missing required parameters. This error also occurs if you include both the tenant name and ID in the request.")
        sys.exit()
    elif r.status_code == 401:
        print("Unauthorized. This error message might indicate any of the following conditions:")
        print("    -You are not authorized to complete this operation.")
        print("    -Additional authentication credentials required. Submit a second authentication request with multi-factor authentication credentials")
        sys.exit()
    elif r.status_code == 403:
        print("User disabled Forbidden")
        print("    -The User disabled message indicates that the request is valid, but the user doesn’t have access to the requested resource. Check with the account administrator to request access.")
        print("    -The Forbidden message might be returned because your account requires multi-factor authentication, and the feature has not been set up. See Request to set up multi-factor authentication on a user account.")
        sys.exit()
    elif r.status_code == 404:
        print("Item not found. The requested resource was not found. The subject token in X-Subject-Token has expired or is no longer available. Use the POST token request to get a new token.")
        sys.exit()
    elif r.status_code == 500:
        print("Service Fault. Service is not available")
        sys.exit()
    else:
        print("Unknown Authentication Error")
        sys.exit

    data = r.json()
    token = (data["access"]["token"]["id"])
    account = (data["access"]["token"]["tenant"]["id"])
    return token,account

#exports image task and checks the status via api
def export_img(token,account,region,container,image):
    create_container(token,account,region,container)

    url = "https://" + region +".images.api.rackspacecloud.com/v2/tasks"
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
    payload = {"type": "export","input":{"image_uuid": image,"receiving_swift_container": container}}

    try:
        r = requests.post(url, headers=headers, json=payload)
    except requests.ConnectionError as e:
        print("Check your interwebs!")
        sys.exit()

        if r.status_code == 201:
            print("Success Request succeeded.")
        elif r.status_code == 400:
            print("A general error has occured.")
            sys.exit()
        elif r.status_code == 401:
            print("Unauthorized")
            sys.exit()
        elif r.status_code == 403:
            print("Forbidden")
            sys.exit()
        elif r.status_code == 405:
            print("Bad Method")
            sys.exit()
        elif r.status_code == 413:
            print("Over Limit 	The number of items returned is above the allowed limit.")
            sys.exit()
        elif r.status_code == 415:
            print("Bad media type. This may result if the wrong media type is used in the cURL request.")
            sys.exit()
        elif r.status_code == 500:
            print("API Fault")
            sys.exit()
        elif r.status_code == 503:
            print("The requested service is unavailable.")
            sys.exit()

    data = r.json()
    task_id = data["id"]
    task_status(token,region,task_id)

def download_img(token, account, region, container, vhd):
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

    try:
        r = requests.get(url,headers=headers, stream=True)
    except requests.ConnectionError as e:
        print("Check your interwebs!")
        sys.exit()

    if r.status_code == 200:
        print("File Found. Starting download")
    else:
        print("File not found. Try again.")
        sys.exit()

    with open(vhd, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()
    #return image

def upload_img(token, account,region, container, vhd):
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

    try:

        with open(vhd, 'rb') as f:
            r = requests.put(url,headers=headers,data=f)
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                bar.show(i + 1)
    except requests.ConnectionError as e:
        print("Check your interwebs!")

    print("Upload Finished.")

#import img task and checks status of task
def import_img(token, region, container, vhd):
    url = "https://" + region +".images.api.rackspacecloud.com/v2/tasks"
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
    payload = {"type": "import","input":{"image_properties": {"name": vhd},"import_from": container + "/" + vhd}}

    try:
        r = requests.post(url, headers=headers, json=payload)
    except requests.ConnectionError as e:
        print("Check your interwebs!")
        sys.exit()

    if r.status_code == 201:
        print("Success Request succeeded.")
    elif r.status_code == 400:
        print("A general error has occured.")
        sys.exit()
    elif r.status_code == 401:
        print("Unauthorized")
        sys.exit()
    elif r.status_code == 403:
        print("Forbidden")
        sys.exit()
    elif r.status_code == 405:
        print("Bad Method")
        sys.exit()
    elif r.status_code == 413:
        print("Over Limit 	The number of items returned is above the allowed limit.")
        sys.exit()
    elif r.status_code == 415:
        print("Bad media type. This may result if the wrong media type is used in the cURL request.")
        sys.exit()
    elif r.status_code == 500:
        print("API Fault")
        sys.exit()
    elif r.status_code == 503:
        print("The requested service is unavailable.")
        sys.exit()
    else:
        print("Unknown Error")
        sys.exit

    data = r.json()
    task_id = data["id"]
    task_status(token,region,task_id)

def update_img(token,region,image):
    url = "https://" + region + ".images.api.rackspacecloud.com/v2/images/" + image
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
    payload = {"op": "add", "path": "vm_mode", "value": "hvm"}
    r = requests.patch(url,headers=headers, json=payload)
    data = r.json()
    print(data)

def task_status(token, region, task_id):
    url = "https://" + region +".images.api.rackspacecloud.com/v2/tasks" + "/" + task_id
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}

    try:
        r = requests.get(url, headers=headers)
    except requests.ConnectionError as e:
        print("Check your interwebs!")
        sys.exit()

    if r.status_code == 201:
        print("Success Request succeeded.")
    elif r.status_code == 400:
        print("A general error has occured.")
        sys.exit()
    elif r.status_code == 401:
        print("Unauthorized")
        sys.exit()
    elif r.status_code == 403:
        print("Forbidden")
        sys.exit()
    elif r.status_code == 405:
        print("Bad Method")
        sys.exit()
    elif r.status_code == 413:
        print("Over Limit 	The number of items returned is above the allowed limit.")
        sys.exit()
    elif r.status_code == 415:
        print("Bad media type. This may result if the wrong media type is used in the cURL request.")
        sys.exit()
    elif r.status_code == 500:
        print("API Fault")
        sys.exit()
    elif r.status_code == 503:
        print("The requested service is unavailable.")
        sys.exit()

    data = r.json()
    status = data["status"]
    while status != 'success'and status != 'failure':
        print(status)
        r = requests.get(url, headers=headers)
        data = r.json()
        status = data["status"]
        time.sleep(15)
        if status == 'failure':
            print("Something went wrong.")
            print(data["message"])

    print(status)

# Checks to see if a container exists. If it doesn't it creats the container.
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

    #Check to see if container exists. If it does  not "status_code == 404" then create the container.
    try:
        r = requests.get(url,headers=headers)
    except requests.ConnectionError as e:
        print("Check your interwebs!")
        sys.exit()

    if r.status_code == 200:
        print("OK. 	The request succeeded.")
    elif r.status_code == 204:
     	print("No Content 	The request succeeded. The server fulfilled the request but does not need to return a body.")
    elif r.status_code == 404:
        print("The requested resource was not found.")
        print("Creating conatiner.")
        try:
            r = requests.put(url, headers=headers)
        except requests.ConnectionError as e:
            print("Check your interwebs!")

        if r.status_code == 201:
            print("Created . The request has been fulfilled. The new container has been created.")
        elif r.status_code == 202:
            print("Accepted 	The request has been fulfilled. For 202 Accepted, the request has been accepted for processing.")
        elif r.status_code == 400:
            print("Bad Request 	The request could not be understood by the server due to malformed syntax.")
        elif r.status_code == 409:
            print("Conflict. The request could not be completed due to a conflict with the current state of the resource.")
            sys.exit()
        else:
            print("Unkown Error")
            sys.exit()

#Create parser to parse command line arguments.
parser = argparse.ArgumentParser()
parser.add_argument("action", help="Actions include: import,export,download, status, upload or update")
parser.add_argument("-u", "--username", help="Rackspace cloud account username.")
parser.add_argument("-p", "--password", help="Rackspace cloud account password.")
parser.add_argument("-i", "--image", help="Image to use for action.")
parser.add_argument("-c", "--container", help="Container to use for action.")
parser.add_argument("-r", "--region", help="Region of the image.")
parser.add_argument("-f", "--file", help="Filename to download/upload.")
args = parser.parse_args()

# get token and account information. function returns a tuple with token and account.
token,account = get_token(args.username,args.password)

# Call function that matches action from user. If user enters an action not listed
# then help will run.
if args.action == "export":
    export_img(token, account, args.region,args.container, args.image)
elif args.action == "import":
    import_img(token, args.region, args.container, args.file)
elif args.action == "download":
    download_img(token, account, args.region, args.container, args.file)
elif args.action == "upload":
    upload_img(token, account, args.region, args.container, args.file)
elif args.action == "update":
    update_img(token, args.region, args.image)
else:
    parser.print_help()
