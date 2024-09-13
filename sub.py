# sub.py

import subprocess
import sys
import os

def print_menu():
    menu_text = """
[ 1 ] XSS Tester | XSS Testing in Hijacked WebViews

Step 1: Select the items you want to test from the extracted CSV file of the app and copy them into test.csv.
Step 2: Fill in the "XSS_payload.txt" file and run the test. 
        *The XSS_payload typically contains a list of XSS filter bypass techniques.
Step 3: You can now monitor the results in real time! 
        *To adjust the execution speed, modify the time.sleep value.

------------------------------------------------------------------------------------------------------------------

[ 2 ] Log Analyzer | Analyze Deeplink URL Call Log with Dumpsys and Logcat

Step 1: Modify the package name and deeplink URL in the "analyze_log.py" script.
Step 2: Statistically analyze the logs recorded during the deeplink URL call process.

-------------------------------------------------------------------------------------------------------------------

[ 3 ] Monitor | Hooking Deeplink, WebView, and JSI Methods While Executing a Deeplink URL

Step 1: Modify the package name and deeplink URL in the "monitor.py" script.
Step 2: Analyze the hooked logs during the deeplink URL execution.
Step 3: While Frida is attached, you can explore and observe the internal reactions of the app.

-------------------------------------------------------------------------------------------------------------------

If Frida is not installed, refer to this link=>

"""
    print(menu_text)

def run_script(script_name):
    try:
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError:
        print(f"Error: Failed to run {script_name}")
    except FileNotFoundError:
        print(f"Error: {script_name} not found")

def main():
    while True:
        print_menu()
        choice = input("Enter your choice (1, 2, 3) or 'q' to quit: ")
        
        if choice == 'q':
            break
        elif choice == '1':
            os.system("start ./XSS_payload.txt" if sys.platform == "win32" else "open ./XSS_payload.txt")
            run_script("./modules/tester/XSS_test.py")
        elif choice == '2':
            os.system("start ./modules/analyzer/analyze_log.py" if sys.platform == "win32" else "open ./modules/analyzer/analyze_log.py")
            run_script("./modules/analyzer/analyze_log.py")
        elif choice == '3':
            os.system("start ./modules/analyzer/monitor.py" if sys.platform == "win32" else "open ./modules/analyzer/monitor.py")
            run_script("./modules/analyzer/monitor.py")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()