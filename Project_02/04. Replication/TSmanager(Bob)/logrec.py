#!/usr/bin/env python3#   Assignment : CPSC-551 Project_02#   Authors    : Rahul Chauhan        (rahulchauhan@csu.fullerton.edu)#                Harshit Singh Rathod (rathod10892@csu.fullerton.edu)#   Program    : subprogram to log and recoverimport yamlimport argparseimport proxyimport jsondef get_file(user):    filename = user + ".yaml"    try:        with open(filename, 'r') as stream:            print(filename)    except IOError:        with open(filename, 'w') as stream:            print(filename)        return filenamedef create_att(tsname, tsevent, tsvalue):    print("Config", tsname, tsevent, tsvalue)    yamnam = get_file(tsname)    ######################################    parser = argparse.ArgumentParser()    parser.add_argument('-c', '--config', metavar='file', type=str, default = yamnam)    args = parser.parse_args()    with open(args.config, 'r') as stream:            restart_chk = yaml.safe_load(stream)    if restart_chk == None:        yamvalue = {'name': f'{tsname}', 'adapter': None, 'filters': []}        with open(args.config, 'w') as stream:            yaml.safe_dump(yamvalue,stream)    if tsevent == "start":        if (restart_chk != None and restart_chk['adapter'] != None):            print("write to tuple")            adapter_uri = restart_chk['adapter']                    ts = proxy.TupleSpaceAdapter(adapter_uri)            print(f'Connected to tuplespace {tsname} on {adapter_uri}')            yamlrecord = restart_chk['filters']            print(len(yamlrecord))            for i in range(0,len(yamlrecord)):                print(yamlrecord[i][0],yamlrecord[i][1])                tuplee = yamlrecord[i][1]                rc = json.loads(tuplee)                if yamlrecord[i][0] == "write":                    ts._out(rc)                if yamlrecord[i][0] == "take":                    ts._in(rc)        else:            print("Tuplespace not up")#    if tsevent == "adapter":        yamvalue = (f'{tsvalue}')        with open(args.config, 'r') as stream:            ada_upd = yaml.safe_load(stream)            ada_upd['adapter'] = yamvalue                    with open(args.config, 'w') as stream:            yaml.safe_dump(ada_upd,stream)#    if (tsevent == "write" or tsevent == "take"):        yamvalue = [f'{tsevent}', f'{tsvalue}']        with open(args.config, 'r') as stream:            fil_upd = yaml.safe_load(stream)            fil_upd['filters'].extend([yamvalue])        with open(args.config, 'w') as stream:            yaml.safe_dump(fil_upd,stream)        return(fil_upd['adapter'])