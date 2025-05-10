import logging

class Client:
    def __init__(self, CompanyName: str, CIF: str, address: str, email: str, phone: int, contact: str, clientID: int = 0):
        self.clientID = clientID
        self.CompanyName = CompanyName
        self.CIF = CIF
        self.address = address
        self.email = email
        self.phone = phone
        self.contact = contact
        
        self.logger = logging.getLogger("appLogger")

    def __repr__(self):
        return (f"Client(clientID={self.clientID}, CompanyName='{self.CompanyName}', CIF={self.CIF}, "
                f"address='{self.address}', email='{self.email}', phone={self.phone}, contact='{self.contact}')")
        
    def getClientJSON(self) -> dict[str, str]:
        """
        Get client information as a JSON object
        """

        # Print the client information as a JSON object
        self.logger.debug(f"Client JSON: {self.__dict__}")        
        
        return {
            "clientID": str(self.clientID),
            "CompanyName": self.CompanyName,
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
        return (self.clientID == 0 and 
                self.CompanyName != "" and
                self.CIF != "" and
                self.address != "" and
                self.email != "" and
                self.phone != 0 and
                self.contact != "")
        