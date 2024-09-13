import subprocess
import time

def check_frida_server():
    cmd = "adb shell \"ps | grep frida\""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return 'frida' in result.stdout

def start_frida_server():
    # Find the Frida server file name
    cmd = "adb shell \"cd /data/local/tmp && ls frida* | head -n 1\""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    frida_server = result.stdout.strip()
    print(f"Frida server filename: {frida_server}")

    # Check and exit existing frida process
    print("Checking for existing Frida processes...")
    cmd = "adb shell \"ps | grep frida | awk '{print $2}'\""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    for pid in result.stdout.split():
        print(f"Terminating existing Frida process with PID: {pid}")
        subprocess.run(f"adb shell \"kill -9 {pid}\"", shell=True)

    time.sleep(2)

    # Start a new Frida server
    print("Starting new Frida server...")
    cmd = f"adb shell \"cd /data/local/tmp && ./{frida_server} &> /dev/null 2>&1\""
    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Verifying the execution of the Frida server
    for _ in range(check_interval):
        time.sleep(1)
        if check_frida_server():
            print("Frida server started!")
            return True

    print("Failed to start Frida server.")
    return False

if __name__ == "__main__":
    while True:
        success = start_frida_server()
        if success:
            print("Frida server is running.")
        else:
            print("Failed to start Frida server.")
        
        user_input = input("Enter 'q' to quit or press Enter to restart Frida server: ")
        if user_input.lower() == 'q':
            break
        print("Restarting Frida server...")