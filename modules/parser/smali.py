import os
from glob import glob


def parseSmali(file_path):
    try:
        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()
    except:
        return [], [], []

    local_register = dict()
    param = set()
    addURI = set()
    UriParse = set()
    method = set()
    addJsIf = set()

    for line in lines:
        line = line.strip()
        words = line.split(" ")

        if words[0] == ".class":
            class_name = line
        elif words[0] == ".method":
            method_name = line

        if ".annotation" in line and "Landroid/webkit/JavascriptInterface" in line:
            method.add(method_name.split(" ")[2].split("(")[0])
        try:
            if "const-string" in line:
                local_register[words[1][:-1]] = words[2].split('"')[1]
            elif "getQueryParameter(" in line:
                if "}" not in line:
                    continue
                var = line.split("}")[0].split()[-1]
                if var in local_register:
                    param.add(local_register[var])
            elif "addURI(" in line:
                var_list = line.split("{")[1].split("}")[0].split(", ")
                if var_list[1] in local_register and var_list[2] in local_register:
                    host = local_register[var_list[1]]
                    path = local_register[var_list[2]]
                    addURI.add(host + "/" + path)
            elif "Uri;->parse(" in line:
                var = line.split("{")[1].split("}")[0]
                if var in local_register:
                    UriParse.add(local_register[var])
            elif "addJavascriptInterface(" in line:
                if "}" not in line:
                    continue
                var_list = line.split("{")[1].split("}")[0].split(", ")
                if var_list[1] in local_register and var_list[2] in local_register:
                    addJsIf.add(local_register[var_list[2]])
        except:
            print(file_path, line)
            exit()
    return list(param), list(addURI), list(UriParse), list(addJsIf), list(method)


def extractSmaliData(decompile_dir, deeplinks):
    params = set()
    addURIs = set()
    UriParses = set()
    tmpUriParse = set()
    addJsIfs = set()
    methods = set()

    for diretory in glob(os.path.join(decompile_dir, "smali*")):
        for path, dirs, files in os.walk(diretory):
            for file in files:
                f = os.path.join(path, file)
                param, addURI, UriParse, addJsIf, method = parseSmali(f)
                if len(param) > 0:
                    params.update(param)
                if len(addURI) > 0:
                    addURIs.update(addURI)
                if len(UriParse) > 0:
                    tmpUriParse.update(UriParse)
                if len(addJsIf) > 0:
                    addJsIfs.update(addJsIf)
                if len(method) > 0:
                    methods.update(method)

    for Uri in tmpUriParse:
        for deeplink in deeplinks:
            if deeplink in Uri:
                UriParses.add(Uri)
                break

    return params, addURIs, UriParses, addJsIfs, methods
