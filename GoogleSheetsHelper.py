from __future__ import print_function

import os.path
import secrets_ 

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class membership(object):
    """
    Helper class for managing the General Membership spreadsheet.
    """

    def __init__(self):

        #GDSC Club Data 23-24 Spreadsheet 
        self.SPREADSHEET_ID = secrets_.spreadsheet.getId()
        self.SPREADSHEET_RANGE = 'General Membership'
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets'] 

        self.refreshCredentials()

    def refreshCredentials(self):
        """
        Logs in the current user in or refreshes credentials if necessary.
        """

        creds = None

        # check for previous sign-in
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
            self.creds = creds

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:

                # first time sign-in
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
                self.creds = creds

            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

    def get_discord_tags(self):
        service = build('sheets', 'v4', credentials=self.creds)
        range_ = self.SPREADSHEET_RANGE + '!E2:E'
        value_render_option = 'FORMATTED_VALUE'

        request = service.spreadsheets().values().get(spreadsheetId=self.SPREADSHEET_ID, 
                                                        range=range_,
                                                        valueRenderOption=value_render_option)
        response = request.execute()
        print(response['values'])

   
   