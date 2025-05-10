import logging

class Client:
    def __init__(self, commercialName: str, CIF: int, address: str, email: str, phone: int, contact: str, clientID: str = ""):
        self.clientID = clientID
        self.commercialName = commercialName
        self.CIF = CIF
        self.address = address
        self.email = email
        self.phone = phone
        self.contact = contact
        
        self.logger = logging.getLogger("appLogger")

    def __repr__(self):
        return (f"Client(clientID={self.clientID}, commercialName='{self.commercialName}', CIF={self.CIF}, "
                f"address='{self.address}', email='{self.email}', phone={self.phone}, contact='{self.contact}')")
        
    def getClientJSON(self) -> dict[str, str]:
        """
        Get client information as a JSON object
        """
        return {
            "clientID": self.clientID,
            "commercialName": self.commercialName,
            "CIF": str(self.CIF),
            "address": self.address,
            "email": self.email,
            "phone": str(self.phone),
            "contact": self.contact
        }
        
    def ready_to_insert(self) -> bool:
        """
        Check if the client is ready to be inserted into the database.
        client is ready if all fields are filled except for clientID
        :return: True if the client is ready, False otherwise.
        """
        return (self.clientID == "" and 
                self.commercialName != "" and
                self.CIF != 0 and
                self.address != "" and
                self.email != "" and
                self.phone != 0 and
                self.contact != "")
        