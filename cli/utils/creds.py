from pathlib import Path
import json


class CredentialsNotFound(Exception):
    def __init__(self):
        self.message = 'Credentials not found'
        super().__init__(self.message)


class Creds():
    def __init__(self, path='.creds.json'):
        self.path = path
        self.creds = Path(self.path)
        if self.creds.exists():
            with open(self.creds, 'r') as f:
                data = json.load(f)
                self.username = data['username']
                self.uid = data['uid']

    def get_username(self):
        return self.username if self.username else CredentialsNotFound()

    def get_uid(self):
        return self.uid if self.uid else CredentialsNotFound()

    def save(self, uid, username):
        return self.creds.write_text(f'{{"uid": "{uid}", "username": "{username}"}}')

    def remove(self):
        if self.creds.exists():
            self.creds.unlink()
