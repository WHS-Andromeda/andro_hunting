import subprocess
import time
import sys
import os

class Config:
    def __init__(self, package_name, deeplink_url):
        self.package_name = package_name
        self.deeplink_url = deeplink_url

def get_path(script_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, '..', 'setup', script_name)

def run_start_frida():
    print("Starting Frida server...")
    start_frida_script = get_path('start_frida.py')
    start_frida_process = subprocess.Popen(['python', start_frida_script], 
                                           stdout=subprocess.PIPE, 
                                           stderr=subprocess.PIPE,
                                           text=True)
    
    while True:
        output = start_frida_process.stdout.readline()
        print(output.strip())
        if "Frida server is running." in output:
            print("Frida server started!")
            return True
        if start_frida_process.poll() is not None:
            print("Error: start_frida.py exited")
            return False

def run_hook_frida(config):
    print("Start Hooking method...")
    hook_frida_script = get_path('hook_frida.py')
    hook_frida_process = subprocess.Popen(['python', hook_frida_script, 
                                           config.package_name, 
                                           config.deeplink_url])
    return hook_frida_process

def main():
    ############# MODIFY HERE: Update the package name and deeplink url as needed ############
    config = Config(
        package_name="com.zhiliaoapp.musically", 
        deeplink_url="https://m.tiktok.com/redirect/webview?url=https%3A%2F%2Fwww.example.com"
    )
    ##########################################################################################

    if run_start_frida():
        time.sleep(2)
        hook_process = run_hook_frida(config)
        hook_process.wait()
    else:
        print("Failed to start Frida server. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()