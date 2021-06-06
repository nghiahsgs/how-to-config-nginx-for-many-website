import io
import os
import subprocess
from slugify import slugify
import sys

def write_file(file_name,ndung):
    f = io.open(file_name, 'w', encoding='utf-8')
    f.write(ndung)
    f.close()


def read_file(file_name):
    f = io.open(file_name, 'r', encoding='utf-8')
    ndung=f.read()
    f.close()
    return ndung


# step 1: create file config in site-available
# domain = 'nghia.com'
# port = 3009
domain = input("Enter your domain (vd nghiahsgs.com): ")
port = input("Enter your port that is running: " )


data = read_file('demo_config_nginx')
data = data.replace('{{domain}}',domain)
data = data.replace('{{port}}','%s'%port)

file_name_0 = '%s.conf'%slugify(domain)
file_name_1 = os.path.join('/etc/nginx/sites-available',file_name_0)
write_file(file_name_1,data)


#step 2: test config file
command = 'sudo nginx -t'
command = command.split(' ')
subprocess.run(command)

#step 3: create symbolic link
file_name_2 = os.path.join('/etc/nginx/sites-enabled',file_name_0)
if os.path.isfile(file_name_2):
    os.remove(file_name_2)

file_name_3 = '/etc/nginx/sites-enabled'
command = 'sudo ln -s %s %s'%(file_name_1,file_name_3)
command = command.split(' ')
subprocess.run(command)

#step 4: restart nginx
command = 'sudo service nginx restart'
command = command.split(' ')
subprocess.run(command)