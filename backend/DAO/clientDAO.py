import psycopg2.extensions
import logging
from client import Client

class ClientDAO:
    def __init__(self, db_connection: psycopg2.extensions.connection):
        """
        Initialize the DAO with a database connection.
        :param db_connection: A database connection object.
        """
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        self.db_connection = db_connection

    def create_client(self, client: Client) -> int:
        """
        Insert a new client into the database.
        :param client: A Client object containing client details.
        :return: The ID of the newly created client.
        """
        query = """
        INSERT INTO clients (clientID, commercialName, CIF, address, email, phone, contact)
        """
        
        logging.debug(f"Creating client: {client}")
        
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (
                client.clientID,
                client.commercialName,
                client.CIF,
                client.address,
                client.email,
                client.phone,
                client.contact
            ))
            result = cursor.fetchone()
            if result is None:
                self.logger.error("Failed to insert client and retrieve its ID.")
                raise ValueError("Failed to insert client and retrieve its ID.")
            client_id = result[0]
            self.db_connection.commit()
            logging.info(f"Client created with ID: {client_id}")
            return client_id
        
    
    def get_client_by_id(self, client_id: int) -> Client:
        """
        Retrieve a client by its ID.
        :param client_id: The ID of the client.
        :return: A Client object containing the client details or None if not found.
        """
        query = "SELECT * FROM clients WHERE clientID = %s"
        
        logging.debug(f"Retrieving client with ID: {client_id}")
        
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (client_id,))
            row = cursor.fetchone()
            if row:
                
                logging.info(f"Client found: {row}")
                return Client(
                    clientID=row[0],
                    commercialName=row[1],
                    CIF=row[2],
                    address=row[3],
                    email=row[4],
                    phone=row[5],
                    contact=row[6]
                )
            else:
                self.logger.error(f"Client with ID {client_id} not found.")
                raise ValueError(f"Client with ID {client_id} not found.")
        
            
            
    def get_all_clients(self) -> list[Client]:
        """
        Retrieve all clients from the database.
        :return: A list of Client objects.
        """
        query = "SELECT * FROM clients"
        
        logging.debug("Retrieving all clients")
        
        with self.db_connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            clients = list[Client]()
        
            for row in results:
                client = Client(
                    clientID=row[0],
                    commercialName=row[1],
                    CIF=row[2],
                    address=row[3],
                    email=row[4],
                    phone=row[5],
                    contact=row[6]
                )
                clients.append(client)
        
            logging.info(f"Retrieved {len(clients)} clients")
            return clients
        
    def update_client(self, client: Client) -> bool:
        """
        Update an existing client in the database.
        :param client: A Client object containing updated client details.
        :return: True if the update was successful, False otherwise.
        """
        query = """
        UPDATE clients
        SET commercialName = %s, CIF = %s, address = %s, email = %s, phone = %s, contact = %s
        WHERE clientID = %s;
        """
        
        logging.debug(f"Updating client: {client}")
        
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (
                client.commercialName,
                client.CIF,
                client.address,
                client.email,
                client.phone,
                client.contact,
                client.clientID
            ))
            self.db_connection.commit()
            
            logging.info(f"Client with ID {client.clientID} updated")
            return cursor.rowcount > 0
        
    def delete_client(self, client_id: int) -> bool:
        """
        Delete a client from the database.
        :param client_id: The ID of the client to delete.
        :return: True if the deletion was successful, False otherwise.
        """
        query = "DELETE FROM clients WHERE clientID = %s"
        
        logging.debug(f"Deleting client with ID: {client_id}")
        
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (client_id,))
            self.db_connection.commit()
            return cursor.rowcount > 0
        
        logging.info(f"Client with ID {client_id} deleted")
        