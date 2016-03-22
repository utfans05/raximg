#!/usr/bin/python
import requests
import time
import argparse
import logging
import sys
from clint.textui import progress
logging.captureWarnings(True)

#Request to authenticate and returns a tuple with token and account number.
def get_token(username,password):
    #setting up api call
    url = "https://identity.api.rackspacecloud.com/v2.0/tokens"
    headers = {'Content-type': 'application/json'}
    payload = {'auth':{'passwordCredentials':{'username': username,'password': password}}}

    #authenticating against the identity
    try:
        r = requests.post(url, headers=headers, json=payload)
    except requests.ConnectionError as e:
        print("Connection Error: Check your interwebs!")
        sys.exit()

    #Check status code. If not sucessful, exit.
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

    #loads json reponse into data as a dictionary.
    data = r.json()
    #assign token and account variables with info from json response.
    token = (data["access"]["token"]["id"])
    account = (data["access"]["token"]["tenant"]["id"])
    return token,account

#Exports image task and checks the status.
def export_img(token,account,region,container,image):
    #Checks whether container exists. If it doesn't  it gets created.
    create_container(token,account,region,container)

    #setting up the api call.
    url = "https://" + region +".images.api.rackspacecloud.com/v2/tasks"
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
    payload = {"type": "export","input":{"image_uuid": image,"receiving_swift_container": container}}

    #Making the api call.
    try:
        r = requests.post(url, headers=headers, json=payload)
    except requests.ConnectionError as e:
        print("Check your interwebs!")
        sys.exit()

        #checks status code from response.
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

    #load json reponse into data
    data = r.json()
    #assign task id from json respons to task_id
    task_id = data["id"]
    print(task_id)
    #check status of task
    task_status(token,region,task_id)

#Downloads vhd file and shows progress bar.
def download_img(token, account, region, container, vhd):
    #Setting up the api call.
    #check region and assign proper endopoint to url.
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

    #api call
    try:
        r = requests.get(url,headers=headers, stream=True)
    except requests.ConnectionError as e:
        print("Check your interwebs!")
        sys.exit()

    #Check status cdoe from response.
    if r.status_code == 200:
        print("File Found. Starting download")
    else:
        print("File not found. Try again.")
        sys.exit()

    #Download file. Clint library is used for the progress bar.
    with open(vhd, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()

#Uploads file to Cloud Files container, progress bar has not been implemented.
def upload_img(token, account,region, container, vhd):
    #Creates container if it does not exist.
    create_container(token,account,region,container)

    #Setting up the api call.
    #check region and assign proper endopoint to url.
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

    #Upload file. Progress bar is not working.
    try:
        with open(vhd, 'rb') as f:
            r = requests.put(url,headers=headers,data=f)
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
                bar.show(i + 1)
    except requests.ConnectionError as e:
        print("Check your interwebs!")

    print("Upload Finished.")

#Import img task and checks status of task.
def import_img(token, region, container, vhd):
    #Setup api call
    url = "https://" + region +".images.api.rackspacecloud.com/v2/tasks"
    headers = {'Content-type': 'application/json', 'X-Auth-Token': token}
    payload = {"type": "import","input":{"image_properties": {"name": vhd},"import_from": container + "/" + vhd}}

    #Making the api call.
    try:
        r = requests.post(url, headers=headers, json=payload)
    except requests.ConnectionError as e:
        print("Check your interwebs!")
        sys.exit()

    #Check status code.
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

    #Loads json reponse as dictionary into data
    data = r.json()
    #Assing task id in order to checks task status.
    task_id = data["id"]
    #Check task status.
    task_status(token,region,task_id)

#Updates the image meta data field vm_mode to hvm.
def update_img(token,region,image):
    #Setting up the api call.
    url = "https://" + region + ".images.api.rackspacecloud.com/v2/images/" + image
    headers = {'Content-Type': 'application/openstack-images-v2.1-json-patch', 'X-Auth-Token': token}
    payload = [{"op": "add", "path": "/vm_mode", "value": "hvm"}]
    #Making the api call. Need to add a try block.
    r = requests.patch(url, json=payload, headers=headers)
    #print responses. Changing this up for only info that is relevant.
    print(r.text)
    print(r.json)

#Checks the status of the export/import task.
def task_status(token, region, task_id):
    #Setup the api call.
    url = "https://" + region +".images.api.rackspacecloud.com/v2/tasks" + "/" + task_id
    headers = {'X-Auth-Token': token}

    #Making the api call. Need to clean up the debug output.
    try:
        r = requests.get(url, headers=headers)
    except requests.ConnectionError as e:
        print("Check your interwebs!")
        sys.exit()

    #Check status code. Need to clean up the debug output.
    print(r.status_code)
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

    #Load json response dictionary into data.
    data = r.json()
    #Check status of export/image task.
    status = data["status"]
    while status != 'success'and status != 'failure':
        print(status)
        r = requests.get(url, headers=headers)

        print(r.status_code)
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
            #sys.exit()

        while True:
            try:
                data = r.json()
                break
            except JSONDecodeError as e:
                time.sleep(10)
                pass
        status = data["status"]
        time.sleep(10)
        if status == 'failure':
            print("Something went wrong.")
            print(data["message"])

    print(status)

# Checks to see if a container exists. If it doesn't, the container is created.
def create_container(token, account, region, container):
    #Setup the api call. Assing proper endpoint to url.
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

    #Check to see if container exists. If not create container.
    try:
        r = requests.get(url,headers=headers)
    except requests.ConnectionError as e:
        print("Check your interwebs!")
        sys.exit()

    #Check status code. If status code is 404, the container will be created.
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

        #Check status code from the put request.
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
parser.add_argument("action", help="Actions include: import,export,download, upload or update")
parser.add_argument("-u", "--username", help="Rackspace cloud account username.")
parser.add_argument("-p", "--password", help="Rackspace cloud account password.")
parser.add_argument("-i", "--image", help="Image to use for action.")
parser.add_argument("-c", "--container", help="Container to use for action.")
parser.add_argument("-r", "--region", help="Region of the image.")
parser.add_argument("-f", "--file", help="Filename to download/upload.")
args = parser.parse_args()

#Get token and account information. function returns a tuple with token and account.
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
