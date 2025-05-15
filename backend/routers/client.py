from fastapi import Depends, APIRouter, HTTPException
from verificator import verifyToken, verifyTokenEmployee
import logging

from DAO.clientDAO import ClientDAO
from DAO.client import Client

router = APIRouter()
clientDAO = ClientDAO()
logger = logging.getLogger("appLogger")

@router.get("/", tags=["client"], dependencies=[Depends(verifyTokenEmployee)])
async def get_all_clients(token: str = Depends(verifyToken)) -> list[dict[str, str]]:
    """
    Get all clients
    """
    logger.debug("Clients requested")
    clients = clientDAO.get_all_clients()
    if not clients:
        return []
    clients_json = [client.getClientJSON() for client in clients]
    logger.debug(f"Clients retrieved: {clients_json}")
    return clients_json

@router.put("/", tags=["client"], dependencies=[Depends(verifyTokenEmployee)])
async def update_client(client: dict[str, str], token: str = Depends(verifyToken)) -> dict[str, str]:
    """
    Update a client
    """
    logger.debug("Client update requested")
    clientId = client["clientID"]
    address = client["address"]
    email = client["email"]
    phone = client["phone"]
    contact = client["contact"]
    logger.debug(f"Client data received for update: {client}")

    actual_client = clientDAO.get_client_by_id(clientId)

    new_client = Client(clientID=int(clientId), CompanyName=actual_client.CompanyName, CIF=actual_client.CIF, address=address, email=email, phone=int(phone), contact=contact)

    # Update the client
    updated_client = clientDAO.update_client(new_client)
    logger.debug(f"Client updated: {updated_client}")
    
    return updated_client.getClientJSON()

@router.post("/", tags=["client"], dependencies=[Depends(verifyTokenEmployee)])
async def create_client(client: dict[str, str], token: str = Depends(verifyToken)) -> dict[str, str]:
    """
    Create a new client
    """     
    logger.debug("Client creation requested")
    CompanyName = client["CompanyName"]
    CIF = client["CIF"]
    address = client["address"]
    email = client["email"]
    phone = client["phone"]
    contact = client["contact"]
    
    new_client = Client( CompanyName=CompanyName, CIF=CIF, address=address, email=email, phone=int(phone), contact=contact)
    
    # Verify the client
    if not new_client.ready_to_insert():
        logger.error("Client verification failed")
        raise HTTPException(status_code=400, detail="Client verification failed, missing fields")
    
    # Create the client
    created_client = clientDAO.create_client(new_client)
    logger.debug(f"Client created: {created_client}")

    return created_client.getClientJSON()