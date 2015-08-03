import pyrax 

pyrax.set_setting("identity_type", "rackspace")

# Start of program. Promtps user for input and returns choice
def menu():
    print('Do you want to export, import or share an image?')
    print('1. Export')
    print('2. Import')
     
    choice = input()
    return choice

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

def download():
    pyrax.set_credentials("txhc4life", "a7ba05b40e6041a1b8f3389416a68c34", region= "DFW")
    obj = pyrax.cloudfiles
    data = obj.get()
    obj.download("/tmp")   

#menu()
#export()
download()
