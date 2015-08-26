import pyrax
import time
import os
import sys
import readline

# export task including creating and verify images and containers
def export_img():
    # ask for imageid, region, and export container
    while True:
        try:
            region = raw_input('What region is the image in? ')
            region = region.upper()

            if region == 'DFW':
                break
            elif region == 'LON':
                break
            elif region == 'HKG':
                break
            elif region == 'IAD':
                break
            elif region == 'SYD':
                break
            else:
                raise


        except KeyboardInterrupt:
            exit()
        except:
            print "Image not found. Try again."

    while True:
        try:
            imageID = raw_input('What is the image id? ')
            imageID = imageID.lower()

            pyrax.set_credentials(username, apiKey, region= region)

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

    container = raw_input('What is the name of the container? ')


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
    task = imgs.export_task(imageID, container)

    # check task status
    task.reload()
    print task.status
    while task.status == "processing":
       time.sleep(1)
       task.reload()

    print "Success"

    #clear screen
    os.system('clear')

def download_vhd():
    # get current working directory
    path = os.getcwd()

    # Download file
    vhd = raw_input("Enter Filename: ")
    region = raw_input("Enter Region: ")
    container = raw_input("Enter Container Name: ")

    print "Verfiying Credentials..."
    pyrax.set_credentials(username, apiKey, region= region)

    print "Downloading..."
    pyrax.cloudfiles.download_object(container, vhd, path)
    print "Success"

    #clear screen
    os.system('clear')

def upload_vhd():
    vhd = raw_input("Enter Filename: ")
    region = raw_input("Enter Region: ")
    container = raw_input("Enter Container Name: ")

    print "Verfiying Credentials..."
    pyrax.set_credentials(username, apiKey, region= region)

    # create container to upload iamge
    print "Creating container " + container + "..."
    cf = pyrax.cloudfiles
    cf.create_container(container)

    print "Uploading " + vhd + "..."
    path = os.getcwd() + "/" + vhd
    chksum = pyrax.utils.get_checksum(path)
    obj = cf.upload_file(container, path, etag=chksum)
    print "Calculated checksum:", chksum
    print "Stored object etag:", obj.etag

def import_img():
    container = raw_input('What is the name of the container? ')
    region = raw_input('What region are you importing to? ')
    region = region.upper()
    vhd = raw_input("What is the file name? ")

    os.system('clear')

    # Verify credentials
    print "Verfiying Credentials..."
    pyrax.set_credentials(username, apiKey, region= region)

    # create container to upload iamge

    print "Importing " + vhd + "..."
    imgs = pyrax.images
    task = imgs.import_task(vhd, container)

    # check task status
    task.reload()
    print task.status
    while task.status == "processing":
       time.sleep(1)
       task.reload()

    print "Success"

    #clear screen
    os.system('clear')

def menu():
    print "Import or Export image?"
    print "1. Export"
    print "2. Import"
    print "3. Download VHD"
    print "4. Upload VHD"
    choice = raw_input(">> ")
    choice = choice.lower()
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
    elif choice in ("q","quit"):
        exit()
    else:
        print "Please enter a 1 or a 2"

    while choice != "q":
        print "Import or Export image?"
        print "1. Export"
        print "2. Import"
        print "3. Download VHD"
        print "4. Upload VHD"
        choice = raw_input(">> ")
        choice = choice.lower()
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
        elif choice in ("q","quit"):
            exit()
        else:
            print "Please enter a 1 or a 2"

pyrax.set_setting("identity_type", "rackspace")

os.system('clear')
# ask user for rackspace credentials
username = raw_input('What is your username? ')
apiKey = raw_input('What is your api key? ')
apiKey = apiKey.lower()

os.system('clear')

menu()
