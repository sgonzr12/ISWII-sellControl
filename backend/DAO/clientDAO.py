import logging

from fastapi import HTTPException

from connect import get_db_connection
from DAO.client import Client

class ClientDAO:
    def __init__(self,):
        """
        Initialize the DAO with a database connection.
        :param db_connection: A database connection object.
        """
        
        self.logger = logging.getLogger("appLogger")
        
        self.db_connection = get_db_connection()
        
        
    def create_client(self, client: Client) -> Client:
        """
        Insert a new client into the database.
        :param client: A Client object containing client details.
        :return: The ID of the newly created client.
        """
        query = """
        INSERT INTO "Clients" ("CompanyName", "CIF", "Address", "Email", "Phone", "Contact")
        values (%s, %s, %s, %s, %s, %s) RETURNING "ClientID";
        """
        
        logging.debug(f"Creating client: {client}")
        
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (
                client.CompanyName,
                client.CIF,
                client.address,
                client.email,
                client.phone,
                client.contact
            ))
            result = cursor.fetchone()
            if result is None:
                self.logger.error("Failed to insert client and retrieve its ID.")
                raise HTTPException(status_code=500, detail="Failed to create client.")
            client_id = result[0]
            self.db_connection.commit()
            
            client.clientID = client_id
            
            logging.info(f"Client created with ID: {client_id}")
            return client

        
    
    def get_client_by_id(self, client_id: str) -> Client:
        """
        Retrieve a client by its ID.
        :param client_id: The ID of the client.
        :return: A Client object containing the client details or None if not found.
        """
        query = """
                SELECT * FROM "Clients" WHERE "ClientID" = %s
                """
                
        logging.debug(f"Retrieving client with ID: {client_id}")
        
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (client_id,))
            row = cursor.fetchone()
            if row:
                
                logging.info(f"Client found: {row}")
                return Client(
                    clientID=row[0],
                    CompanyName=row[1],
                    CIF=row[2],
                    address=row[3],
                    email=row[4],
                    phone=row[5],
                    contact=row[6]
                )
            else:
                self.logger.error(f"Client with ID {client_id} not found.")
                raise HTTPException(status_code=404, detail=f"Client with ID {client_id} not found.")
        
            
            
    def get_all_clients(self) -> list[Client]:
        """
        Retrieve all clients from the database.
        :return: A list of Client objects.
        """
        query = """
                SELECT * FROM "Clients"
                """
        
        logging.debug("Retrieving all clients")
        
        with self.db_connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            clients = list[Client]()
        
            for row in results:
                client = Client(
                    clientID=row[0],
                    CompanyName=row[1],
                    CIF=row[2],
                    address=row[3],
                    email=row[4],
                    phone=row[5],
                    contact=row[6]
                )
                clients.append(client)
        
            logging.info(f"Retrieved {len(clients)} clients")
            return clients
        
    def update_client(self, client: Client) -> Client:
        """
        Update an existing client in the database.
        :param client: A Client object containing updated client details.
        :return: True if the update was successful, False otherwise.
        """
        query = """
        UPDATE "Clients"
        SET "CompanyName" = %s, "CIF" = %s, "Address" = %s, "Email" = %s, "Phone" = %s, "Contact" = %s
        WHERE "ClientID" = %s;
        """
        
        logging.debug(f"Updating client: {client}")
        
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (
                client.CompanyName,

                client.CIF,
                client.address,
                client.email,
                client.phone,
                client.contact,
                client.clientID
            ))
            self.db_connection.commit()
            
            logging.info(f"Client with ID {client.clientID} updated")
            if cursor.rowcount == 0:
                self.logger.error(f"Failed to update client with ID {client.clientID}.")
                raise HTTPException(status_code=404, detail=f"Client with ID {client.clientID} not found.")
            return client
        
    def delete_client(self, client_id: int) -> bool:
        """
        Delete a client from the database.
        :param client_id: The ID of the client to delete.
        :return: True if the deletion was successful, False otherwise.
        """
        query = """DELETE FROM "Clients" WHERE "ClientID" = %s
        """
        
        logging.debug(f"Deleting client with ID: {client_id}")
        
        with self.db_connection.cursor() as cursor:
            cursor.execute(query, (client_id,))
            self.db_connection.commit()
            return cursor.rowcount > 0
        
        logging.info(f"Client with ID {client_id} deleted")
        