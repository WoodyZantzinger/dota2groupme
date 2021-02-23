# -*- coding: utf-8 -*
import logging
import traceback

from googleapiclient import discovery

from .CooldownResponse import *
import random
from utils import get_groupme_messages
from utils import GroupMeMessage
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive# Rename the downloaded JSON file to client_secrets.json
import urllib.request


GROUPMEME_FOLDER = "groupmemes"
SUN_UPLOADS_FOLDER = "sUN_uploads"

class ResponseSave(ResponseCooldown):
    COOLDOWN = -1
    RESPONSE_KEY = "#save"
    SUN_UPLOADS_FOLDER_ID = ''

    def __init__(self, msg):
        super(ResponseSave, self).__init__(msg, self, ResponseSave.COOLDOWN)


    def get_referenced_image_urls(self):
        if not hasattr(self.msg, "attachments"):
            return

        attachments = self.msg.attachments

        found_quoted_message = False
        for attachment in attachments:
            if "reply_id" in attachment and attachment['type'] == "reply":
                found_quoted_message = True
                break

        if not found_quoted_message:
            return

        reply_id = attachment['reply_id']
        group_id = self.msg.group_id

        msg = get_groupme_messages.get_exact_group_message(group_id, reply_id)
        msg = msg['response']['message']
        image_attachments = []
        if "attachments" in msg:
            for attachment in msg['attachments']:
                if attachment['type'] == "image":
                    image_attachments.append(attachment)
        return image_attachments

    def upload_files_to_pydrive(self, local_fnames):
        YAML_FNAME = "settings.yaml"
        SAVED_CREDS_FNAME = "credentials.json"

        print("== GETTING SECRETS FROM DB ==")
        secrets_data = self.get_response_storage("client_secrets")
        secrets_data = secrets_data[1:-1].replace("\\n", '\n')

        credentials = self.get_response_storage("credentialsjson")
        credentials = credentials[1:-1].replace("\\n", '\n')

        settingsyaml = self.get_response_storage("settingsyaml")
        print("loaded yaml = ")
        print(settingsyaml)
        settingsyaml = settingsyaml[1:-1].replace("\\n", '\n')

        if secrets_data:
            with open("client_secrets.json", "w+") as f:
                f.write(secrets_data)
                pass
            pass
        if credentials:
            with open(SAVED_CREDS_FNAME, "w+") as f:
                f.write(credentials)
                pass
            pass
        if settingsyaml:
            with open(YAML_FNAME, "w+") as f:
                f.write(settingsyaml)
                pass
            pass

        print("== WRITING SECRETS TO FILES ==")

        logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
        logging.getLogger('googleapiclient.discovery').setLevel(logging.CRITICAL)

        gauth = GoogleAuth()

        try:
            gauth.LoadCredentialsFile(SAVED_CREDS_FNAME)
            if gauth.credentials is None:
                # Authenticate if they're not there
                gauth.LocalWebserverAuth()
            elif gauth.access_token_expired:
                # Refresh them if expired
                gauth.Refresh()
        except Exception as e:
            traceback.print_exc()
            gauth.Authorize()
        # Save the current credentials to a file

        gauth.SaveCredentialsFile(SAVED_CREDS_FNAME)
        with open(SAVED_CREDS_FNAME) as f:
            creds = f.read()
        if creds:
            creds = "'" + creds + "'"
            self.set_response_storage("credentialsjson", creds)
        with open(YAML_FNAME, 'r') as f:
            yaml = f.read()
        if yaml:
            yaml = "'" + yaml + "'"
            self.set_response_storage("settingsyaml", yaml)

        drive = GoogleDrive(gauth)  # List files in Google Drive

        # 1) Choose your starting point by inserting file name
        folder_title = SUN_UPLOADS_FOLDER
        folder_id = ''
        if not ResponseSave.SUN_UPLOADS_FOLDER_ID:
            print("== SEEKING SUN UPLOADS FOLDER ==")
            # 2) Retrieve the folder id - start searching from root
            file_list = drive.ListFile({'q': "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()

            print(f"len(file_list) = {len(file_list)}")
            for file in file_list:
                if (file['title'] == folder_title):
                    ResponseSave.SUN_UPLOADS_FOLDER_ID = file['id']
                    break
        else:
            print(f"== USING SAVED FOLDER_ID = {ResponseSave.SUN_UPLOADS_FOLDER_ID}")


        for fname in local_fnames:
            file = drive.CreateFile({'parents': [{'id': ResponseSave.SUN_UPLOADS_FOLDER_ID}]})
            file.SetContentFile(fname)
            file.Upload()



    def _respond(self):
        image_attachments = self.get_referenced_image_urls()
        filenames = self.save_images_to_local(image_attachments)
        self.upload_files_to_pydrive(filenames)
        return f"Uploaded {len(filenames)} to Groupmemes"

    def save_images_to_local(self, image_attachments):
        local_fnames = []
        for attachment in image_attachments:
            uuid = attachment['url'].split('.')[-1]
            fname = attachment['url'][:(-1 * (len(uuid)+1))]
            ftype = fname.split('.')[-1]
            save_fname = "".join([uuid, '.', ftype])
            urllib.request.urlretrieve(attachment['url'],
                                       save_fname)
            local_fnames.append(save_fname)
        return local_fnames