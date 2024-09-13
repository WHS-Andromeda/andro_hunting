import os, time, re
import xml.etree.ElementTree as ET


def screen_xml_root_get():
    os.system("adb shell uiautomator dump /sdcard/screen.xml")
    os.system("adb pull /sdcard/screen.xml")
    return ET.parse("screen.xml").getroot()


def playsotre_apk_download(app_name):
    dnldPath = f"data/apk/{app_name}.apk"
    list_package = os.popen(f"adb shell pm path {app_name}").read()
    apk_file_name = list_package.split("\n")[0].split(":")[-1]
    os.system(f"adb pull {apk_file_name} {dnldPath}")
    print(f"[+] done. file saved to apks/[playstore]{app_name}")


def wait_installation():
    cnt = 0
    while True:
        root = screen_xml_root_get()
        cnt += 1
        if cnt == 100:
            os.system("adb shell am force-stop com.android.vending")
            time.sleep(3)
            return False
        if not root:
            return False
        done_button_found = any(
            ("Uninstall" == node.get("text", "")) for node in root.iter("node")
        )
        if done_button_found:
            print("Installation finished.")
            return True
        time.sleep(3)


def playstore_download(package_name):
    dnldPath = f"data/apk/{package_name}.apk"
    os.makedirs(os.path.dirname(dnldPath), exist_ok=True)
    print(f"[+] starting download for {package_name}")
    os.system(
        f"adb shell am start market://details?id={package_name}"
    )  # Run the Google Play Store page
    time.sleep(3)
    root = screen_xml_root_get()
    for node in root.iter("node"):
        text = node.get("text", "")
        if "Install" in text:
            install_button_bounds = node.get("bounds")
            install_button_xy = [
                int(num) for num in re.findall(r"\d+", install_button_bounds)
            ]
            os.system(
                f"adb shell input tap {install_button_xy[0]} {install_button_xy[1]}"
            )
            res = wait_installation()
            if res:
                playsotre_apk_download(package_name)
                break
        elif "Uninstall" in text:
            playsotre_apk_download(package_name)
            break
