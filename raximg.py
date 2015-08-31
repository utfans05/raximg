import pyrax
import time
import os
import os.path
import sys
import readline

# export task including creating and verify images and containers
def export_img():
    # get region
    region = region_check()

    pyrax.set_credentials(username, apiKey, region= region)

    imageID = image_check()

    container = raw_input('What is the name of the container? ')

    os.system('clear')

    # create container
    print "Creating container " + container + "..."
    cf = pyrax.cloudfiles
    cf.create_container(container)

    # export image
    print "Exporting " + imageID + "..."
    task = imgs.export_task(imageID, container)

    # check task status
    task.reload()
    print task.status

    while task.status == "pending":
        time.sleep(10)
        task.reload

    print task.status

    while task.status == "processing":
        time.sleep(10)
        task.reload()

    if task.status == "failure":
        print task.message
    else:
        print "Export Task Successful..."

    main_menu = raw_input("Return to Main Menu(Y/N): ")
    main_menu = main_menu.lower()

    if main_menu == "y":
       os.system('clear')
       menu()
    elif main_menu == "yes":
       os.system('clear')
       menu()
    else:
       exit()

def download_vhd():
    # get current working directory
    path = os.getcwd()
    # Download file
    region = region_check()

    pyrax.set_credentials(username, apiKey, region= region)

    while True:
        try:
            container = raw_input("Enter Container Name: ")
            if container in pyrax.cloudfiles.list_containers():
                print "Found Container."
                break
            else:
                raise
        except KeyboardInterrupt:
            menu()
        except:
              print "Container not found. Try again."


    cf = pyrax.cloudfiles
    cont = cf.get_container(container)
    cont = cont.get_objects()
    container_list = ''.join(str(e) for e in cont)

    while True:
        vhd = raw_input("Enter Filename: ")
        if vhd in container_list:
            print "File found"
            break
        else:
            print "File not found. Try again"

    while True:
        try:
            print "Downloading..."
            pyrax.cloudfiles.download_object(container, vhd, path)

        except KeyboardInterrupt:
            print "Download Canceled."
            menu()

        except Exception,e:
            print e
            retry = raw_input("Download failed. Try again. (Y/N): ")
            if retry.lower() in ("yes" or "y"):
                pass
            else:
                menu()
        else:
            break

    print "Success!"

    main_menu = raw_input("Return to Main Menu(Y/N): ")
    main_menu = main_menu.lower()

    if main_menu == "y":
       os.system('clear')
       menu()
    elif main_menu == "yes":
       os.system('clear')
       menu()
    else:
       exit()

def upload_vhd():
    region = region_check()

    pyrax.set_credentials(username, apiKey, region= region)

    container = raw_input("Enter Container Name: ")

    while True:
        try:
            vhd = raw_input("Enter Filename: ")
            path = os.getcwd() + "/" + vhd
            if os.path.isfile(path):
                print "File found"
                break
            else:
                raise
        except:
            print "File not foudn. Try Again"


    # create container to upload iamge
    print "Creating container " + container + "..."
    cf = pyrax.cloudfiles
    cf.create_container(container)

    print "Uploading " + vhd + "..."
    chksum = pyrax.utils.get_checksum(path)
    obj = cf.upload_file(container, path, etag=chksum)
    print "Calculated checksum:", chksum
    print "Stored object etag:", obj.etag

def import_img():
    region = region_check()

    pyrax.set_credentials(username, apiKey, region= region)

    while True:
        try:
            container = raw_input('What is the name of the container? ')

            if container in pyrax.cloudfiles.list_containers():
                print "Found Container."
                break
            else:
                raise
        except KeyboardInterrupt:
                exit()
        except:
                print "Container not found. Try again"

    cf = pyrax.cloudfiles
    cont = cf.get_container(container)
    cont = cont.get_objects()
    container_list = ''.join(str(e) for e in cont)

    while True:
        try:
            vhd = raw_input("What is the file name? ")

            if vhd in container_list:
                print "File found"
                break
            else:
                raise
        except:
            print "File not found. Try again."

    os.system('clear')

    # create container to upload iamge
    print "Importing " + vhd + "..."
    imgs = pyrax.images
    task = imgs.import_task(vhd, container)

    # check task status
    task.reload()
    print task.status
    while task.status == "processing":
       time.sleep(10)
       task.reload()

    print "Success"

    #clear screen
    os.system('clear')

def region_check():
    while True:
        try:
            region = raw_input('What region is the image in? ')
            region = region.upper()

            if region in ['DFW','LON','ORD','HKG','IAD','SYD']:
                break
            else:
                raise

        except KeyboardInterrupt:
            exit()
        except:
            print "Region not found. [DFW,LON,ORD,HKG,IAD,SYD]."

    return region

def image_check():
    while True:
        try:
            imageID = raw_input('What is the image id? ')
            imageID = imageID.lower()

            global imgs
            imgs = pyrax.images
            imglist = imgs.list_all()
            imglist = ''.join(str(e) for e in imglist)

            if imageID in imglist:
                print "Found Image"
                break
            else:
                raise
        except KeyboardInterrupt:
            exit()
        except:
            print "Image does not exist"

    return imageID

def menu():
    while True:
        print "Import or Export image?"
        print "1. Export"
        print "2. Import"
        print "3. Download VHD"
        print "4. Upload VHD"
        choice = raw_input(">> ")

        os.system('clear')

        if choice == "1":
            export_img()
            menu()
        elif choice == "2":
            import_img()
            menu()
        elif choice == "3":
            download_vhd()
            menu()
        elif choice == "4":
            upload_vhd()
            menu()
        elif choice.lower() in ("q","quit","exit"):
            exit()
        else:
            print "Please enter a 1, 2, 3, or 4. Q to quit."

pyrax.set_setting("identity_type", "rackspace")

os.system('clear')
# ask user for rackspace credentials
username = raw_input('What is your username? ')
apiKey = raw_input('What is your api key? ')
apiKey = apiKey.lower()

os.system('clear')

menu()
