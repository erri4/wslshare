import subprocess
import re

def get_all_wifi_passwords():
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'],
                                capture_output=True)
        
        output = result.stdout.decode('cp850', errors='ignore')
        
        profiles = re.findall(r"(?:All User Profile)\s*:\s*(.*)", output)
        
        if not profiles:
            print("Raw output:")
            print(output)
            return "No Wi-Fi profiles found."
        
        wifi_passwords = {}
        for profile in profiles:
            profile = profile.strip()
            result = subprocess.run(['netsh', 'wlan', 'show', 'profile', 
                                     f'name={profile}', 'key=clear'],
                                    capture_output=True)
            
            profile_output = result.stdout.decode('cp850', errors='ignore')
            password_match = re.search(r'(?:Key Content)\s*:\s*(.*)', profile_output)
            password = password_match.group(1).strip() if password_match else "No password found"
            wifi_passwords[profile] = password
        
        return wifi_passwords
    except Exception as e:
        return f"Error: {e}"

wifi_passwords = get_all_wifi_passwords()
if isinstance(wifi_passwords, dict):
    print("\nSaved Wi-Fi Passwords:\n")
    for wifi, password in wifi_passwords.items():
        print(f"Wi-Fi Name: {wifi}  |  Password: {password}")
else:
    print(wifi_passwords)