***WIP

Rewriting this script using requests. Images are building out once exported to another region. Image exporting causes image meta data to be changed. Some vm's require the vm_mode set to hvm to build correctly. The export task defaults to xen in the vm_mode meta data. The meta data can be changed via the rackspace api or the nova/glance client.

USAGE:
positional arguments:
  action                

Actions include: import,export,download, status,
                        upload or update

optional arguments:

  -h, --help            show this help message and exit

  -u USERNAME, --username USERNAME
                        Rackspace cloud account username.

  -p PASSWORD, --password PASSWORD
                        Rackspace cloud account password.

  -i IMAGE, --image IMAGE
                        Image to use for action.

  -c CONTAINER, --container CONTAINER
                        Container to use for action.

  -r REGION, --region REGION
                        Region of the image.

  -f FILE, --file FILE  Filename to download/upload.

EXAMPLE:
raximg export -u $username -p $password -r $region -c $container -i $image 
