import os
import json
import mintapi
import pandas as pd
import gspread
import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials

print("Starting budget app...")

with open("mint_credentials.json") as cred:
	mint_credentials = json.load(cred)

username = mint_credentials['mint_username']
password = mint_credentials['mint_password']

mint = mintapi.Mint(
    username,  # Email used to log in to Mint
    password,  # Your password used to log in to mint
 
    # Optional parameters
    mfa_method='sms',  # Can be 'sms' (default), 'email', or 'soft-token'.
                       # if mintapi detects an MFA request, it will trigger the requested method
                       # and prompt on the command line.
    headless=False,  # Whether the chromedriver should work without opening a
                     # visible window (useful for server-side deployments)
    mfa_input_callback=None,  # A callback accepting a single argument (the prompt)
                              # which returns the user-inputted 2FA code. By default
                              # the default Python `input` function is used.
    session_path=None, # Directory that the Chrome persistent session will be written/read from.
                       # To avoid the 2FA code being asked for multiple times, you can either set
                       # this parameter or log in by hand in Chrome under the same user this runs
                       # as.
    imap_account=None, # account name used to log in to your IMAP server
    imap_password=None, # account password used to log in to your IMAP server
    imap_server=None,  # IMAP server host name
    imap_folder='INBOX',  # IMAP folder that receives MFA email
    wait_for_sync=False,  # do not wait for accounts to sync
    wait_for_sync_timeout=300,  # number of seconds to wait for sync
)

transactions = mint.get_transactions()
transactions = transactions.drop(["labels", 'notes', 'original_description'], axis=1)
transactions.loc[(transactions.transaction_type == 'debit'), 'transaction_type'] = 'Expense'
transactions.loc[(transactions.transaction_type == 'credit'), 'transaction_type'] = 'Income'
transactions = transactions[transactions.category != 'credit card payment']

transactions_sheet_url = "https://docs.google.com/spreadsheets/d/1yYy1UZvkdywkON3Q6TQMd6s2cWZJswY9VkEoDGD3TB8/edit#gid=0"

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('sheets_credentials.json', scope)
client = gspread.authorize(creds)
# Send the data to google sheets
spreadsheet_key = transactions_sheet_url
d2g.upload(transactions,spreadsheet_key,"RAW_DATA",credentials=creds,row_names=True)