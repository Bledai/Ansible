from ansible.module_utils.basic import *

import psutil
#from lxml import html
import requests
import re
import json

def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return proc.as_dict(attrs=['username', 'pid'])

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False





def main():
    module = AnsibleModule(
        argument_spec=dict(
            process_name=dict(type='str'),
            port=dict( type=int),
            url=dict(type='str'),
            regex=dict(type='str')
          #  url=dict(required=True, type='str')
        )
    )
    process_name = module.params["process_name"]
    port = module.params['port']
    url = module.params["url"]
    regex = module.params['regex']

    result = dict(
        msg='',
        changed=False,
        process_name='',
        port='',
        regex_in_url=''
    )
    if process_name is not None:
        if checkIfProcessRunning(process_name) is False:
            result['msg'] = 'process not running'

        else:
            result['changed'] = True
            result['process_name'] = checkIfProcessRunning(process_name)
            if port is not None:
                result['msg'] = port
                if getAllports(result['process_name']['pid'], port):
                    result['port'] = 'LISTEN'
    if url is not None:
        result['changed'] = True
        result['regex_in_url'] = getUrlcontent(url,regex)
    return module.exit_json(**result)


def getAllports(pid, port):
    proc = psutil.Process(pid)
    stat = proc.connections()
    for st in stat:
        if port == st[3][1] and st[5] == 'LISTEN':
            return True
    return False

url = 'https://vk.com/'
def getUrlcontent(url, regex='.*'):
    page = requests.get('https://vk.com/')
    print (type(page.content))
    return re.findall('login', page.content)

print (getUrlcontent(url,'login'))
#process = checkIfProcessRunning('java')
#stat = getAllports(process['pid'], 6942)

#main()
