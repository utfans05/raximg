import pyrax
import time
import os
import sys
import readline
import getpass

pyrax.set_setting("identity_type", "rackspace")

# export task including creating and verify images and containers
def export_img():
    # ask user for rackspace credentials
    username = raw_input('What is your username? ')
    apiKey = raw_input('What is your api key? ')
    apiKey = apiKey.lower()

    # ask for imageid, region, and export container
    imageID = raw_input('What is the image id? ')
    imageID = imageID.lower()
    container = raw_input('What is the name of the container? ')
    region = raw_input('What region is the image in? ')
    region = region.upper()

    os.system('clear')

    # set credentials and default region
    print "Verfiying Credentials..."
    pyrax.set_credentials(username, apiKey, region= region)

    # create container
    print "Creating container " + container + "..."
    cf = pyrax.cloudfiles
    cf.create_container(container)

    # export image
    print "Exporting " + imageID + "..."
    imgs = pyrax.images
    task = imgs.export_task(imageID, container)

    # check task status
    task.reload()
    print task.status
    while task.status == "processing" or "pending":
       time.sleep(20)
       task.reload()

    # append vhd extention to image
    vhd = imageID + ".vhd"

    # get current working directory
    path = os.getcwd()

    # Download file
    print "Downlading " + vhd + "..."
    pyrax.cloudfiles.download_object(container, vhd, path)

    print "Success"

    #clear screen
    os.system('clear')


def import_img():
    # get credentials
    # ask user for rackspace credentials
    username = raw_input('What is your username? ')
    apiKey = raw_input('What is your api key? ')
    apiKey = apiKey.lower()
    container = raw_input('What is the name of the container? ')
    region = raw_input('What region are you importing to? ')
    region = region.upper()
    vhd = raw_input("What is the file name? ")

    os.system('clear')

    # Verify credentials
    print "Verfiying Credentials..."
    pyrax.set_credentials(username, apiKey, region= region)

    # create container to upload iamge
    print "Creating container " + container + "..."
    cf = pyrax.cloudfiles
    cf.create_container(container)

    print "Uploading " + vhd + "..."
    pth = os.getcwd() + "/" + vhd
    chksum = pyrax.utils.get_checksum(pth)
    obj = cf.upload_file(container, pth, etag=chksum)
    print "Calculated checksum:", chksum
    print "Stored object etag:", obj.etag

    print "Importing " + vhd + "..."
    imgs = pyrax.images
    task = imgs.import_task(vhd, container)

    # check task status
    task.reload()
    print task.status
    while task.status == "processing" or "pending":
       time.sleep(20)
       task.reload()

    print "Success"

    #clear screen
    os.system('clear')

def menu():
    print "Import or Export image?"
    print "1. Export"
    print "2. Import"
    choice = raw_input(">> ")
    choice = choice.lower()
    os.system('clear')

    if choice == "1":
        export_img()
        menu()
    elif choice == "2":
        import_img()
        menu()
    elif choice in ("q","quit"):
        exit()
    else:
        print "Please enter a 1 or a 2"

    while choice != "q":
        print "Import or Export image?"
        print "1.Export"
        print "2.Import"
        choice = raw_input(">> ")
        choice = choice.lower()
        os.system('clear')

        if choice == "1":
            export_img()
            menu()
        elif choice == "2":
            import_img()
            menu()
        elif choice in ("q", "quit"):
            exit()
        else:
            print "Please enter a 1 or a 2"

os.system('clear')
menu()
