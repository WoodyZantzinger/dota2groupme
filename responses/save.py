# -*- coding: utf-8 -*
import asyncio
import logging
import traceback

from googleapiclient import discovery

from .CooldownResponse import *
import random
from utils import get_groupme_messages
from utils import GroupMeMessage
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive  # Rename the downloaded JSON file to client_secrets.json
import urllib.request

GROUPMEME_FOLDER = "groupmemes"
SUN_UPLOADS_FOLDER = "sUN_uploads"


class ResponseSave(ResponseCooldown):
    COOLDOWN = -1
    RESPONSE_KEY = "#save"
    SUN_UPLOADS_FOLDER_ID = ''

    def __init__(self, msg):
        super(ResponseSave, self).__init__(msg, self, ResponseSave.COOLDOWN)

    def get_referenced_image_urls(self): # @TODO rework this for new APIs
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

        if not len(local_fnames):
            return

        YAML_FNAME = "settings.yaml"
        SAVED_CREDS_FNAME = "credentials.json"

        # Get secrets from DB, then store them to disk
        # Heroku storage is ephemeral, so it's important to write them each time
        # Lastly, storing JSON as a string is probably dumb, but it needs to be prefixed
        # and suffixed with a `'` (single quote). That's why you see the [1:-1] below.
        secrets_data = self.get_response_storage("client_secrets")
        secrets_data = secrets_data[1:-1].replace("\\n", '\n')
        credentials = self.get_response_storage("credentialsjson")
        credentials = credentials[1:-1].replace("\\n", '\n')
        settings_yaml = self.get_response_storage("settingsyaml")
        settings_yaml = settings_yaml[1:-1].replace("\\n", '\n')

        # Go ahead and write those to a file. w+ on each open() call means that
        # the file will be erased if opened at all, so comment out the whole "with" clause
        # if you want to persist the settings across runs of #save

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
        if settings_yaml:
            with open(YAML_FNAME, "w+") as f:
                f.write(settings_yaml)
                pass
            pass

        # Google API has some weird logging configuration that barks at you for no real reason...
        logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
        logging.getLogger('googleapiclient.discovery').setLevel(logging.CRITICAL)

        # Now, use those saved auth files to login. First, try and use the files we saved. If that fails,
        # then reauthenticate manually (Exception clause). This is a real pain on Heroku, as it sends the
        # OAuth authorization URI to Heroku's logs. You'll have to dig it out of there, or get the service running
        # locally and then push to live.
        # Fortunately, Google API supports multiple callback domains, so both localhost:5000 and young-fortress-3393
        # are both accepted.
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

        # save the credentials that result from the auth process to a file, then save that file out to the
        # database again. Prefix and suffix each file with ' so it stores properly.
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

        # Use authentication to get access to Google Drive
        drive = GoogleDrive(gauth)

        # We need the SUN_UPLOADS_FOLDER's {id} to put the images into that folder. This is pretty slow,
        # so we cache the ID. If the dyno gets rebooted, then it'll need to be pulled again.
        if not ResponseSave.SUN_UPLOADS_FOLDER_ID:
            file_list = drive.ListFile(
                {'q': "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
            for file in file_list:
                if file['title'] == SUN_UPLOADS_FOLDER:
                    ResponseSave.SUN_UPLOADS_FOLDER_ID = file['id']
                    break
        else:
            print(f"== USING SAVED FOLDER_ID = {ResponseSave.SUN_UPLOADS_FOLDER_ID}")

        for fname in local_fnames:
            file = drive.CreateFile({'parents': [{'id': ResponseSave.SUN_UPLOADS_FOLDER_ID}]})
            file.SetContentFile(fname)
            file.Upload()

    def _respond(self):
        image_attachments = []
        image_attachments = asyncio.new_event_loop().run_until_complete(
            self.msg.save_attachments_to_local()
        )
        filenames = image_attachments # self.save_images_to_local(image_attachments)
        self.upload_files_to_pydrive(filenames)
        return f"Uploaded {len(filenames)} to Groupmemes"

    def save_images_to_local(self, image_attachments):
        local_fnames = []
        for attachment in image_attachments:
            uuid = attachment['url'].split('.')[-1]
            fname = attachment['url'][:(-1 * (len(uuid) + 1))]
            ftype = fname.split('.')[-1]
            save_fname = "".join([uuid, '.', ftype])
            urllib.request.urlretrieve(attachment['url'],
                                       save_fname)
            local_fnames.append(save_fname)
        return local_fnames
