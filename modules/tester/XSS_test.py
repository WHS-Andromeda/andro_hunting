import os
import time
import csv
import urllib.parse

def read_csv(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
        
        scheme_hosts = list(set(row['Scheme and Host'] for row in data if row['Scheme and Host']))
        parameters = list(set(row['Parameter'] for row in data if row['Parameter']))
        
        return scheme_hosts, parameters

def read_xss(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def redirect_test(deeplink, xss_payload):
    if not deeplink:
        print("Error: Empty deeplink, Skipping test!")
        return
    encoded_payload = urllib.parse.quote(xss_payload, safe='') #urlencoding 
    test_url = f"{deeplink}{encoded_payload}"
    cmd = f'adb shell am start -W -a android.intent.action.VIEW -c android.intent.category.BROWSABLE -d "{test_url}"'
    print(f"Executing command: {cmd}")
    os.system(cmd)

    time.sleep(5) #You can Adjust delay time 

    os.system(f"adb shell input keyevent 3")

def main():
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_DIR = os.path.join(CURRENT_DIR, '..', '..', 'data', 'csv', 'test.csv')
    XSS_DIR = os.path.join(CURRENT_DIR, '..', '..', 'XSS_payload.txt')
    
    scheme_hosts, parameters = read_csv(CSV_DIR)
    xss_payloads = read_xss(XSS_DIR)

    for scheme_host in scheme_hosts:
        for parameter in parameters:
            deeplink = f"{scheme_host}?{parameter}="
            print(f"\nCreated deeplink: {deeplink}")

            for xss_payload in xss_payloads:
                print(f"\nTesting deeplink: {deeplink}")
                print(f"Scheme and Host: {scheme_host}")
                print(f"Parameter: {parameter}")
                print(f"XSS Payload: {xss_payload}")
                
                redirect_test(deeplink, xss_payload)
                
                time.sleep(2)

if __name__ == "__main__":
    main()