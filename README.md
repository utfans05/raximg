WIP

Rewriting this script using requests. Images are building out once exported to another region. Image exporting causes image meta data to be changed. Some vm's require the vm_mode set to hvm to build correctly. The export task defaults to xen in the vm_mode meta data. The meta data can be changed via the rackspace api or the nova/glance client.
