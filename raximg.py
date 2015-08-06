import pyrax 
import time

pyrax.set_setting("identity_type", "rackspace")

# export task including creating and verify images and containers
def export():
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
       task.reload()
       print task.status
       time.sleep(60)

#def download():
    # Function to download image
    #username = raw_input('What is your username? ')
    #apiKey = raw_input('What is your api key? ')
    #region = "DFW"
   
    #pyrax.set_credentials(username, apiKey, region= region)

    #pyrax.cloudfiles.download_object()

export()
#import()
#download()
