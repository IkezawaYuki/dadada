import hubspot


class HubspotClient:
    def __init__(self, access_token):
        self.client = hubspot.HubSpot(access_token)

    def create_ticket(self):
        pass
