import pyrax 
import time
import os

pyrax.set_setting("identity_type", "rackspace")

# export task including creating and verify images and containers
def export_img():
    # ask user for rackspace credentials
    username = raw_input('What is your username? ')
    apiKey = raw_input('What is your api key? ')

    # ask for imageid, region, and export container
    imageID = raw_input('What is the image id? ')
    container = raw_input('What is the name of the container? ')
    region = raw_input('What region is the image in? ')
    
    # set credentials and default region
    pyrax.set_credentials(username, apiKey, region= region)

    # create container
    cf = pyrax.cloudfiles
    cf.create_container(container)

    # export image
    imgs = pyrax.images
    task = imgs.export_task(imageID, container)

    # check if image is done uplaoding and progress 
    # Once done jump to download process
    task.reload()
    while task.status == "processing":
       time.sleep(60)
       task.reload()
       print task.status

    vhd = imageID + ".vhd"   
     

    path = os.getcwd()
    # Download file   
    pyrax.cloudfiles.download_object(container, vhd, path)


def import_img():
    # get credentials
    # ask user for rackspace credentials
    username = raw_input('What is your username? ')
    apiKey = raw_input('What is your api key? ')
    container = raw_input('What is the name of the container? ')
    region = raw_input('What region are you importing to? ')
    vhd = raw_input("What is the file name? ")

    pyrax.set_credentials(username, apiKey, region= region)

     # create container to upload iamge
    cf = pyrax.cloudfiles
    cf.create_container(container)

    pth = os.getcwd() + "/" + vhd
    chksum = pyrax.utils.get_checksum(pth)
    obj = cf.upload_file(container, pth, etag=chksum)
    print "Calculated checksum:", chksum
    print "Stored object etag:", obj.etag

    imgs = pyrax.images
    task = imgs.import_task(vhd, container)

    task.reload()
    while task.status == "processing":
       time.sleep(60)
       task.reload()
       print task.status

print "Import or Export image?"
print "1. Export"
print "2. Import"
choice = raw_input()

if choice == "1": 
    export_img()
else: 
    import_img()


#import_img()
#download_vhd()
#upload_vhd()