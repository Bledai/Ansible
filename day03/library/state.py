from ansible.module_utils.basic import *

import psutil


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
            process_name=dict(required=True, type='str'),
            port=dict( type=int)
          #  url=dict(required=True, type='str')
        )
    )
    process_name = module.params["process_name"]
    port = module.params['port']
   # url = module.params["url"]

    result = dict(
        msg='',
        changed=False,
        process_name='',
        port=''
    )
    if checkIfProcessRunning(process_name) is False:
        result['msg'] = 'process not running'

    else:
        result['changed'] = True
        result['process_name'] = checkIfProcessRunning(process_name)
        if port is not None:
            result['msg'] = port
            if getAllports(result['process_name']['pid'], port):
                result['port'] = 'LISTEN'
    return module.exit_json(**result)


def getAllports(pid, port):
    proc = psutil.Process(pid)
    stat = proc.connections()
    for st in stat:
        if port == st[3][1] and st[5] == 'LISTEN':
            return True
    return False

#process = checkIfProcessRunning('java')
#stat = getAllports(process['pid'], 6942)

main()
