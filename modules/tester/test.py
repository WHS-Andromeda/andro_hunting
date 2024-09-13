import os
import time


def openDeeplink(deeplink):
    cmd = f"adb shell am start -a android.intent.action.VIEW -c android.intent.category.BROWSABLE -d {deeplink}"
    os.system(cmd)
    print(cmd)
    print(deeplink)
    time.sleep(3.5)

    os.system(f"adb shell input keyevent 3")


def testDeeplink(deeplinks, params, redirectUrl):
    for deeplink in deeplinks:
        for param in params:
            dl = f"{deeplink}?{param}={redirectUrl}?trigger={deeplink}?{param}"
            print(dl)
            openDeeplink(dl)
