# -*- coding: utf-8 -*-

# syntax: {"controller": {"function": "controllers.name.function"}, ... }

# function call: url.address[a][c][f](a, b, c=1)

def get_function(url):
    vars = {}
    args = []
    if url.startswith("/"):
        url = url[1:]
    tmp_args = url.split("/")
    for i, arg in enumerate(tmp_args):
        if i == 0:
            a = arg
        elif i == 1:
            c = arg
        elif i == 2:
            # nevermind the extension
            f = arg.split(".")[0]
        elif i > 2:
            if "?" in arg:
                tmp_index = arg.find("?")
                if tmp_index != 0:
                    args.append(arg[:tmp_index])
                    arg = arg[tmp_index:]
                tmp_vars = arg.replace("?", "")
                kv_str = tmp_vars.split("&")
                for kv in kv_str:
                    tmp_kv = kv.split("=")
                    vars[tmp_kv[0]] = tmp_kv[1]
            else:
                args.append(arg)

    print "Link: ", a, c, f, args, vars
    return a, c, f, args, vars
