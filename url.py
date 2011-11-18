# -*- coding: utf-8 -*-

# syntax: {"controller": {"function": "controllers.name.function"}, ... }

# function call: url.address[a][c][f](a, b, c=1)

def get_function(url):
    vars = {}
    args = []

    get_pos = url.find("?")

    if  get_pos >= 0:
        url_address = url[:get_pos]
        get_vars = url[get_pos +1:]
    else:
        get_vars = ""
        url_address = url
    
    if url_address.startswith("/"):
        url_address = url_address[1:]
        
    tmp_args = url_address.split("/")

    for i, arg in enumerate(tmp_args):
        if i == 0:
            a = arg
        elif i == 1:
            c = arg
        elif i == 2:
            # nevermind the extension
            f = arg.split(".")[0]
        elif i > 2:
            args.append(arg)

    if get_vars != "":
        """
        tmp_index = arg.find("?")
        if tmp_index != 0:
            args.append(arg[:tmp_index])
            arg = arg[tmp_index:]
        tmp_vars = arg.replace("?", "")
        """
        kv_str = get_vars.split("&")
        for kv in kv_str:
            tmp_kv = kv.split("=")
            if len(tmp_kv) > 1:
                vars[tmp_kv[0]] = tmp_kv[1]
                
    return a, c, f, args, vars


def create_address(data):
    # returns a relative project
    # url as a string from url
    # data
    url = None
    if len(data) == 5:
        address = [data[0], data[1], data[2]] + [arg for arg in data[3]]
        url = "/".join(address)
        if len(data[4]) > 0:
            url += "?"
            for k, v in data[4].iteritems():
                url += k + "=" + v + "&"
            url = url[:-1]

    return url