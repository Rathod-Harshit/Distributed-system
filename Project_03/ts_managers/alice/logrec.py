#!/usr/bin/env python3

#   Assignment : CPSC-551 Project_03
#   Authors    : Harshit Singh Rathod (rathod10892@csu.fullerton.edu)
#   Program    : subprogram to log and recover

import yaml
import argparse

import proxy
import json



def get_file(user):
    filename = user + ".yaml"
    try:
        with open(filename, 'r') as stream:
            print(filename)

    except IOError:
        with open(filename, 'w') as stream:
            print(filename)
    
    return filename

def create_att(tsname, tsevent, tsordr, tsvalue):

    #print("Config", tsname, tsevent, tsordr, tsvalue)
    yamnam = get_file(tsname)

    ######################################

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', metavar='file', type=str, default = yamnam)
    args = parser.parse_args()

    with open(args.config, 'r') as stream:
            restart_chk = yaml.safe_load(stream)

    if restart_chk == None:
        yamvalue = {'name': f'{tsname}', 'adapter': None, 'filters': []}

        with open(args.config, 'w') as stream:
            yaml.safe_dump(yamvalue,stream)



    if tsevent == "start":

        if (restart_chk != None and restart_chk['adapter'] != None):

            adapter_uri = restart_chk['adapter']        
            ts = proxy.TupleSpaceAdapter(adapter_uri)

            print(f'Connected to tuplespace {tsname} on {adapter_uri}')

            yamlrecord = restart_chk['filters']
            print(len(yamlrecord))
            ts._reset(0)

            for i in range(0,len(yamlrecord)):

                tuplee = yamlrecord[i][2]
                rc = json.loads(tuplee)

                if yamlrecord[i][1] == "write":
                    ts._out(rc,int(yamlrecord[i][0]))

                if yamlrecord[i][1] == "take":
                    ts._in(rc,int(yamlrecord[i][0]))
        else:
            #print("Adapter not up")
            pass
#

    if tsevent == "adapter":

        yamvalue = (f'{tsvalue}')

        with open(args.config, 'r') as stream:
            ada_upd = yaml.safe_load(stream)
            ada_upd['adapter'] = yamvalue
            

        with open(args.config, 'w') as stream:
            yaml.safe_dump(ada_upd,stream)
            
        ts = proxy.TupleSpaceAdapter(tsvalue)
        ts._reset(tsordr)

#

    if (tsevent == "write" or tsevent == "take"):

        yamvalue = [f'{tsordr}', f'{tsevent}', f'{tsvalue}']

        with open(args.config, 'r') as stream:
            fil_upd = yaml.safe_load(stream)
            fil_upd['filters'].extend([yamvalue])

        with open(args.config, 'w') as stream:
            yaml.safe_dump(fil_upd,stream)

        return(fil_upd['adapter'])

#

    if tsevent == "lag":
        yamlrecord = restart_chk['filters']
        adapter_uri = restart_chk['adapter']        
        ts = proxy.TupleSpaceAdapter(adapter_uri)
        for i in range(0,len(yamlrecord)):
            if yamlrecord[i][0] >= tsordr:
                tuplee = yamlrecord[i][2]
                rc = json.loads(tuplee)

                if yamlrecord[i][1] == "write":
                    ts._out(rc,int(yamlrecord[i][0]))

                if yamlrecord[i][1] == "take":
                    ts._in(rc,int(yamlrecord[i][0]))
