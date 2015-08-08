import pyrax 
import time

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
       

def download_vhd():
    #Function to download image
    username = raw_input('What is your username? ')
    apiKey = raw_input('What is your api key? ')
    region = raw_input('What region is the image in? ')
   
    pyrax.set_credentials(username, apiKey, region= region)

    pyrax.cloudfiles.download_object(region, file ,directory)

def upload_vhd():
    ##upload image to container

    # get credentials
    # ask user for rackspace credentials
    username = raw_input('What is your username? ')
    apiKey = raw_input('What is your api key? ')

    # ask for imageid, region, and export container
    #fileName = raw_input('Where is the file located? ')
    container = raw_input('What is the name of the container? ')
    region = raw_input('What region are you importing to? ')

    pyrax.set_credentials(username, apiKey, region= region)

    # create container to upload iamge
    cf = pyrax.cloudfiles
    cf.create_container(container)

    pth = path to file
    chksum = pyrax.utils.get_checksum(pth)
    obj = cf.upload_file("example", pth, etag=chksum)
    print "Calculated checksum:", chksum
    print "Stored object etag:", obj.etag

def import_img():
    # get credentials
    # ask user for rackspace credentials
    username = raw_input('What is your username? ')
    apiKey = raw_input('What is your api key? ')
    container = raw_input('What is the name of the container? ')
    region = raw_input('What region are you importing to? ')

    pyrax.set_credentials(username, apiKey, region= region)

    imgs = pyrax.images
    task = imgs.import_task(, container)

    task.reload()
    while task.status == "processing":
       time.sleep(60)
       task.reload()
       print task.status


#export_img()
#import_img()
#download_vhd()
#upload_vhd()