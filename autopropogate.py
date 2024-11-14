import subprocess  # We'll use this to run commands in the shell
import sys  # To check which Python version is running
import urllib.request  # To download stuff from the web
import os  # To handle file paths and check if files exist
import json  # For reading/writing JSON data

def install_and_run_py_script():
    # Check if we're on Python 3 or higher
    if sys.version_info < (3, 0):
        print('Python 3 not detected. Installing...')
        # Run a PowerShell command to install Python 3 (Windows only, needs admin access)
        subprocess.call([
            'powershell.exe', 
            'Start-Process', 'python', 
            '-ArgumentList', '/quiet', '-Wait', '-NoNewWindow', '-PassThru', 
            '-Verb', 'runas'
        ])
        print('Python 3 installation complete.')

    # Try to load Google Drive API credentials from a JSON file
    creds = None
    if os.path.exists('credentials.json'):
        with open('credentials.json', 'r') as f:
            creds = json.load(f)
    
    # If creds weren’t loaded, stop and ask for the JSON file
    if not creds:
        print('Google Drive API credentials not found. Please download the JSON file and place it in the current directory.')
        return
    
    # Import Google API credentials (should be installed separately)
    from google.oauth2.credentials import Credentials
    creds = Credentials.from_authorized_user_info(info=creds)

    # Set up the URL and filename for the script we want to download from GitHub
    url = 'https://raw.githubusercontent.com/RosaJosh/joshsfiles/main/autopropogate.py'
    filename = 'autopropogate.py'

    print(f'Downloading {filename} from {url}...')
    urllib.request.urlretrieve(url, filename)

    # Run the downloaded Python script
    print(f'Running {filename}...')
    subprocess.call(['python', filename])
