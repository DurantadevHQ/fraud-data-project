#!/usr/bin/env python3
"""
Fraud-Data GDrive Sync - Automated backup system
"""

import os
import json
import logging
import argparse
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/backup.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Authentication scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']

class GoogleDriveBackup:
    def __init__(self, credentials_path='config/credentials.json'):
        self.credentials_path = credentials_path
        self.service = self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google Drive API"""
        creds = None
        token_path = 'config/token.json'
        
        if os.path.exists(token_path):
            try:
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            except Exception as e:
                logger.warning(f"Token load error: {e}")
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    logger.error(f"Token refresh failed: {e}")
                    creds = None
            
            if not creds:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                except Exception as e:
                    logger.error(f"Authentication failed: {e}")
                    raise
            
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        
        return build('drive', 'v3', credentials=creds)
    
    def upload_file(self, file_path, folder_id=None):
        """Upload a file to Google Drive"""
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None
        
        file_name = os.path.basename(file_path)
        file_metadata = {
            'name': file_name,
            'description': f'Fraud-data-project backup {datetime.now().isoformat()}',
            'mimeType': 'application/gzip'
        }
        
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        try:
            media = MediaFileUpload(
                file_path,
                mimetype='application/gzip',
                resumable=True
            )
            
            logger.info(f"Starting upload: {file_name}")
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink, size'
            ).execute()
            
            logger.info(f"Upload successful: {file['name']} (ID: {file['id']})")
            logger.info(f"File accessible at: {file.get('webViewLink', 'N/A')}")
            
            return file
            
        except HttpError as error:
            logger.error(f"Google Drive API error: {error}")
            return None
        except Exception as error:
            logger.error(f"Upload failed: {error}")
            return None

def main():
    parser = argparse.ArgumentParser(description='Fraud-Data GDrive Sync')
    parser.add_argument('file_path', help='Path to the backup file to upload')
    parser.add_argument('--folder-id', help='Google Drive folder ID')
    
    args = parser.parse_args()
    
    try:
        drive = GoogleDriveBackup()
        drive.upload_file(args.file_path, args.folder_id)
            
    except Exception as e:
        logger.error(f"Backup process failed: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
