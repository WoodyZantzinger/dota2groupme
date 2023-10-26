import random
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Google Drive folder ID containing the pictures
PICTURE_FOLDER_ID = '1Geoad4AjPHxZgb_d7PveHoK2VzZIlR4E'

def authenticate_google_drive():
    gauth = GoogleAuth()
    # Try to load saved credentials, or initiate a new authentication process if not found
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive

def get_random_picture_url(drive):
    picture_files = drive.ListFile({'q': f"'{PICTURE_FOLDER_ID}' in parents"}).GetList()
    
    if not picture_files:
        return None

    random_picture = random.choice(picture_files)
    return random_picture['downloadUrl']

def main():
    # Authenticate with Google Drive
    drive = authenticate_google_drive()

    # Get a random picture URL
    random_picture_url = get_random_picture_url(drive)

    if random_picture_url:
        # You can now post the random picture URL to your desired platform
        print(f"Random Picture URL: {random_picture_url}")
    else:
        print("No pictures found in the specified folder.")

if __name__ == '__main__':
    main()
