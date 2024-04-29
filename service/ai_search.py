from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient


class AiSearch:
    def __init__(self, service_endpoint, index_name, api_key):
        self.client = SearchClient(service_endpoint, index_name, AzureKeyCredential(api_key))

    def push(self, doc):
        result = self.client.upload_documents(documents=doc)
        return result[0].succeeded
