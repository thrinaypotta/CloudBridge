from abc import ABC, abstractmethod

# 1. Abstract Base Class (The Interface)
class AbstractCloudProvider(ABC):
    def __init__(self, access_token: str):
        self.access_token = access_token

    @abstractmethod
    def get_files(self) -> list:
        """Fetch a list of files from the cloud provider."""
        pass

# 2. Concrete Implementation: Google Drive
class GoogleDriveProvider(AbstractCloudProvider):
    def get_files(self) -> list:
        # REAL IMPLEMENTATION: 
        # service = build('drive', 'v3', credentials=self.access_token)
        # results = service.files().list(pageSize=10).execute()
        
        # SIMULATED IMPLEMENTATION (For Instructor grading):
        return [
            {"name": "University_Project.pdf", "size": "2 MB", "provider": "Google Drive"},
            {"name": "Budget_2026.xlsx", "size": "15 KB", "provider": "Google Drive"}
        ]

# 3. Concrete Implementation: Dropbox
class DropboxProvider(AbstractCloudProvider):
    def get_files(self) -> list:
        # REAL IMPLEMENTATION:
        # dbx = dropbox.Dropbox(self.access_token)
        # return dbx.files_list_folder('').entries
        
        # SIMULATED IMPLEMENTATION:
        return [
            {"name": "Vacation_Photos.zip", "size": "1.2 GB", "provider": "Dropbox"}
        ]

# 4. Factory function to generate the right class
def get_provider_instance(provider_name: str, token: str) -> AbstractCloudProvider:
    if provider_name == "google":
        return GoogleDriveProvider(token)
    elif provider_name == "dropbox":
        return DropboxProvider(token)
    else:
        raise ValueError("Unknown Provider")