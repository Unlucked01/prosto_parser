import google
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
import pygsheets
from googleapiclient.errors import HttpError

# Замените на путь к вашему JSON-ключу аутентификации и ID каталога Google Drive, в который вы хотите загрузить файл
SERVICE_ACCOUNT_FILE = 'creds.json'
DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
SPREAD_SHEET_ID = os.getenv("DRIVE_FOLDER_ID")


def authenticate():
    return service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)


def upload_file(file_paths):
    file_links = []
    for file_path in file_paths:
        creds = authenticate()
        service = build('drive', 'v3', credentials=creds)
        file_metadata = {
            'name': file_path,
            'parents': [DRIVE_FOLDER_ID]
        }
        file = service.files().create(body=file_metadata, media_body=file_path, fields='id').execute()
        print('File ID: %s' % file.get('id'))
        file_link = f"https://drive.google.com/file/d/{file.get('id')}/view?usp=drive_link"
        file_links.append(file_link)
    return file_links


def write(df):
    creds, _ = google.auth.default()
    try:
        service = build("sheets", "v4", credentials=creds)
        body = {"values": df}
        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=SPREAD_SHEET_ID,
                range=('A1','*'),
                body=body,
            )
            .execute()
        )
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    df = pd.DataFrame(
                        {
                                "Text": "123123123123",
                                "Links": "asddadsadsa"
                        }
    )
    write(df)