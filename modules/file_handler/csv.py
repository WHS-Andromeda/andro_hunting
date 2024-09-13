import os, csv

def saveCSV(activity_name, deeplink, package_name, csv_dir, params=None):
    os.makedirs(csv_dir, exist_ok=True)
    csv_file = os.path.join(csv_dir, f"{package_name}.csv")
    
    file_exists = os.path.exists(csv_file)
    
    with open(csv_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Package", "Activity", "Scheme and Host", "Parameter"])
        
        if params:
            params = list(set(params))  
            params.sort()  
        
        params_str = ','.join(params) if params else ""
        writer.writerow([package_name, activity_name, deeplink, params_str])
    