import os
import time
import subprocess
from datetime import datetime

################### MODIFY HERE: Update the package name and deeplink url as needed ###########################

PACKAGE_NAME = "com.zhiliaoapp.musically" #package name of app 
DEEPLINK_URL = "https://m.tiktok.com/redirect/webview?url=https%3A%2F%2Fwww.example.com" #deeplink test payload 

###############################################################################################################

class Log:
    def __init__(self):
        self.dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'logs'))
        os.makedirs(self.dir, exist_ok=True)
        self.analyze_file = os.path.join(self.dir, f"analyze_log_{datetime.now():%Y%m%d_%H%M%S}.txt")

    def write(self, msg, is_error=False):
        with open(self.analyze_file, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} - {'ERROR: ' if is_error else ''}{msg}\n")
        print(msg)

log = Log()

def run_command(command):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        if error:
            log.write(f"Command error: {error.decode()}", is_error=True)
        return output, error
    except Exception as e:
        log.write(f"Error running command: {e}", is_error=True)
        return None, str(e)

def test_redirection():
    cmd = f'adb shell am start -W -a android.intent.action.VIEW -c android.intent.category.BROWSABLE -d "{DEEPLINK_URL}"'
    log.write(f"Executing command: {cmd}")
    os.system(cmd)
    time.sleep(3)

def launch_app():
    cmd = f'adb shell monkey -p {PACKAGE_NAME} -c android.intent.category.LAUNCHER 1'
    log.write(f"Launching app: {cmd}")
    os.system(cmd)
    time.sleep(4)  

def collect_dumpsys():
    dumpsys_cmd = f'adb shell "dumpsys activity activities | grep -i {PACKAGE_NAME} | grep -i Hist"'
    dumpsys_output, _ = run_command(dumpsys_cmd)
    if dumpsys_output:
        log.write("Dumpsys Output:")
        log.write(dumpsys_output.decode())
    else:
        log.write("No dumpsys output collected", is_error=True)

def collect_logcat():
    pid_cmd = f'adb shell "pidof {PACKAGE_NAME}"'
    pid, _ = run_command(pid_cmd)
    
    if pid:
        logcat_cmd = f'adb logcat -d *:W'
        logcat_output, _ = run_command(logcat_cmd)
        if logcat_output:
            log.write("Logcat Output:")
            log.write(logcat_output.decode())
        else:
            log.write("No logcat output collected", is_error=True)
    else:
        log.write(f"Could not find PID for {PACKAGE_NAME}", is_error=True)

def main():
    log.write(f"Package Name: {PACKAGE_NAME}")
    log.write(f"Test URL: {DEEPLINK_URL}")
    
    os.system('adb logcat -c')

    test_redirection()
    
    launch_app()
    
    collect_dumpsys()
    collect_logcat()
        
    time.sleep(2)

    log.write(f"Analysis complete. Log file: {log.analyze_file}")

if __name__ == "__main__":
    main()