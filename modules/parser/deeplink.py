import xml.etree.ElementTree as ET
from modules.file_handler.csv import saveCSV


def getStringValue(strings_dict, name):
    if name and name.startswith("@string/"):
        string_name = name.split("/")[1]
        return strings_dict.get(string_name, "")
    return name or ""


def parseStringFromXml(strings_file):
    strings_dict = dict()

    tree = ET.parse(strings_file)
    root = tree.getroot()

    for string in root.findall("string"):
        key = string.get("name")
        value = string.text
        strings_dict[key] = value

    return strings_dict


def extractDeeplinks(scheme_list, host_list, path_list):
    deeplink = ""
    if not scheme_list:
        scheme_list = [""]
    if not host_list:
        host_list = [""]
    if not path_list:
        path_list = [""]
    deeplinks = []

    for scheme in scheme_list:
        for host in host_list:
            for path in path_list:
                if scheme and host:
                    deeplink = f"{scheme}{host}{path}"
                elif scheme and not host:
                    deeplink = f"{scheme}"
                deeplinks.append(deeplink)
    return deeplinks


def parseDeeplinks(package_name, csv_dir, manifest_file, strings_file):
    result = set()
    strings_dict = parseStringFromXml(strings_file)

    tree = ET.parse(manifest_file)
    root = tree.getroot()

    for activity in root.findall(".//activity"):
        activity_name = activity.get("{http://schemas.android.com/apk/res/android}name")
        for intent_filter in activity.findall("intent-filter"):
            deeplink = ""
            scheme_list = []
            host_list = []
            path_list = []
            for data in intent_filter.findall("data"):
                scheme = data.get(
                    "{http://schemas.android.com/apk/res/android}scheme", ""
                )
                if scheme and scheme.startswith("@string/"):
                    scheme = strings_dict.get(scheme.split("@string/")[1])
                if scheme:
                    scheme_list.append(scheme + "://")

                host = data.get("{http://schemas.android.com/apk/res/android}host", "")
                if host and host.startswith("@string/"):
                    host = strings_dict.get(host.split("@string/")[1])
                if host:
                    host_list.append(host)

                path_prefix = data.get(
                    "{http://schemas.android.com/apk/res/android}pathPrefix", ""
                )
                if path_prefix and path_prefix.startswith("@string/"):
                    path_prefix = strings_dict.get(path_prefix.split("@string/")[1])
                if path_prefix:
                    path_list.append(path_prefix)

                path_pattern = data.get(
                    "{http://schemas.android.com/apk/res/android}pathPattern", ""
                )
                if path_pattern and path_pattern.startswith("@string/"):
                    path_pattern = strings_dict.get(path_pattern.split("@string/")[1])
                if path_pattern:
                    path_list.append(path_pattern)

                path = data.get("{http://schemas.android.com/apk/res/android}path", "")
                if path and path.startswith("@string/"):
                    path = strings_dict.get(path.split("@string/")[1])
                if path:
                    path_list.append(path)

            for deeplink in extractDeeplinks(scheme_list, host_list, path_list):
                if deeplink != "" and deeplink.find("http") == -1:
                    print(f"[{activity_name}] : {deeplink}")
                    result.add(deeplink)
                    saveCSV(activity_name, deeplink, package_name, csv_dir)

    return list(result)
