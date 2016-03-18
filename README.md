This script is not supported by Rackspace. I am learning python and using this project to practice what I am learning. Advise and code contributions are welcomed.

***WIP

PVHVM cloud servers require the image meta data field vm_mode to be set to hvm, in order to build correctly. The export task changes most of the meta data and the default value for vm_mode is xen. To change the vm_mode field to hvm you can use the update action.

USAGE:
positional arguments:
  action

Actions include: import,export,download, status,upload or update.

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
raximg update -u $username -p $password -r $region -i $image
