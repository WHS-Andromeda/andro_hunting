from urllib.parse import urlparse


def filterDeeplinks(deeplink: list):
    blacklist_keywords = {
        "firebase",
        "mailto",
        "fb",
        "recaptcha",
        "smsto",
        "fbconnect",
        "kakao",
        "onelink",
        "naver",
        "utm",
    }
    result = []

    for link in deeplink:
        parsed_url = urlparse(link)
        if parsed_url.netloc:
            if not any(keyword in link for keyword in blacklist_keywords):
                result.append(link)

    return list(set(result))
