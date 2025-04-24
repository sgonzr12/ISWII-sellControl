class Client:
    def __init__(self, clientID: int, commercialName: str, CIF: int, address: str, email: str, phone: int, contact: str):
        self.clientID = clientID
        self.commercialName = commercialName
        self.CIF = CIF
        self.address = address
        self.email = email
        self.phone = phone
        self.contact = contact

    def __repr__(self):
        return (f"Client(clientID={self.clientID}, commercialName='{self.commercialName}', CIF={self.CIF}, "
                f"address='{self.address}', email='{self.email}', phone={self.phone}, contact='{self.contact}')")