def filterParams(params: list):
    blacklist_keywords = {"utm", "error", "type", "title"}
    result = []

    for param in params:
        if not any(keyword in param for keyword in blacklist_keywords):
            result.append(param)

    return list(set(result))
