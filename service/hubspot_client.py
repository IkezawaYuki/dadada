import hubspot
from hubspot import HubSpot
from hubspot.crm.tickets import SimplePublicObjectInput, PublicObjectSearchRequest
from hubspot.crm.associations import PublicAssociation, BatchInputPublicAssociation


class HubspotClient:
    def __init__(self, access_token):
        self.client = HubSpot(api_access_token=access_token)

    def associate(self, ticket_id, contact_id):

        # アソシエーションを作成
        association = PublicAssociation(
            from_id=ticket_id,
            to_id=contact_id,
            type_id=15  # Ticket to Contact association type
        )

        # バッチ入力でアソシエーションを作成する
        associations = BatchInputPublicAssociation(
            inputs=[association]
        )

        try:
            # アソシエーションの実行
            self.client.crm.associations.batch_api.create("tickets", associations)
            print("Association created successfully")
        except Exception as e:
            print("An error occurred:", e)

    def search_contact(self, email_address):
        search_query = {
            "filterGroups": [
                {
                    "filters": [
                        {
                            "propertyName": "email",
                            "operator": "EQ",
                            "value": email_address
                        }
                    ]
                }
            ],
            "limit": 1
        }

        contacts_search_result = self.client.crm.contacts.search_api.do_search(
            public_object_search_request=PublicObjectSearchRequest(**search_query)
        )

        result = None
        for contact in contacts_search_result.results:
            result = contact.to_dict()
            print("Contact ID:", contact.id)
            return contact.id
        return result

    def create_ticket(self, content):
        create_ticket_id = None
        try:
            ticket = SimplePublicObjectInput(
                properties={
                    "hs_pipeline": "0",
                    "hs_pipeline_stage": "1",
                    "subject": "お問い合わせがありました",
                    "content": content,
                    "hs_ticket_priority": "high"
                }
            )
            created_ticket = self.client.crm.tickets.basic_api.create(ticket)
            print("Ticket created successfully:", created_ticket.id)
            create_ticket_id = created_ticket.id
        except Exception as e:
            print(e)
        return create_ticket_id

