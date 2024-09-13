import time
import subprocess
import os
from datetime import datetime
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
default_script = os.path.join(current_dir, "..", "script", "monitor.js")
timeout = 100

class Log:
    def __init__(self):
        self.dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'logs'))
        os.makedirs(self.dir, exist_ok=True)
        self.frida_file = os.path.join(self.dir, f"frida_log_{datetime.now():%Y%m%d_%H%M%S}.txt")
        
    def write(self, msg, is_error=False):
        file = self.error_file if is_error else self.frida_file
        with open(file, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} - {msg}\n")
        print(msg)

log = Log()

def run_cmd(cmd, shell=True):
    try:
        result = subprocess.run(cmd, shell=shell, check=True, text=True, capture_output=True)
        log.write(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        log.write(f"Command error: {e}", is_error=True)
        return False

def run_frida(package_name, deeplink_url):
    log.write("Attaching Frida and launching deep link...")
    frida_cmd = f"frida -U -f {package_name} -l {default_script}"
    deeplink_cmd = f"adb shell am start -a android.intent.action.VIEW -c android.intent.category.BROWSABLE -d {deeplink_url}"
    
    try:
        frida_process = subprocess.Popen(frida_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        time.sleep(3)
        
        run_cmd(deeplink_cmd)
        
        start_time = time.time()
        while True:
            if time.time() - start_time > timeout:
                log.write("timeout. Terminating process.", is_error=True)
                frida_process.terminate()
                return False
            
            output = frida_process.stdout.readline()
            if output == '' and frida_process.poll() is not None:
                break
            if output:
                log.write(output.strip())
        
        stderr_output = frida_process.stderr.read()
        if stderr_output:
            log.write(f"Frida error output: {stderr_output}", is_error=True)
        
        rc = frida_process.poll()
        log.write(f"Frida process exited with return code: {rc}")
        return True
    
    except Exception as e:
        log.write(f"Error: {e}", is_error=True)
        return False

def main():
    if len(sys.argv) != 3:
        log.write("Usage: python hook_frida.py <package_name> <deeplink_url>", is_error=True)
        sys.exit(1)

    package_name = sys.argv[1]
    deeplink_url = sys.argv[2]

    run_frida(package_name, deeplink_url)

if __name__ == "__main__":
    main()
    log.write("\nBYE!")