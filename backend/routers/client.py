from fastapi import Depends, APIRouter, HTTPException
from verificator import verifyToken, verifyTokenEmployee

from DAO.clientDAO import ClientDAO
from DAO.client import Client

router = APIRouter()
clientDAO = ClientDAO()

@router.get("/", tags=["client"], dependencies=[Depends(verifyTokenEmployee)])
async def get_all_clients(token: str = Depends(verifyToken)) -> list[dict[str, str]]:
    """
    Get all clients
    """
    print("Clients requested")
    clients = clientDAO.get_all_clients()
    return [client.getClientJSON() for client in clients]

@router.put("/", tags=["client"], dependencies=[Depends(verifyTokenEmployee)])
async def update_client(client: dict[str, str], token: str = Depends(verifyToken)) -> dict[str, str]:
    """
    Update a client
    """
    print("Client update requested")
    clientId = client["clientID"]
    address = client["address"]
    email = client["email"]
    phone = client["phone"]
    contact = client["contact"]
    
    actual_client = clientDAO.get_client_by_id(clientId)
    
    
    new_client = Client(clientID=int(clientId), CompanyName=actual_client.CompanyName, CIF=actual_client.CIF, address=address, email=email, phone=int(phone), contact=contact)
    
    # Update the client
    updated_client = clientDAO.update_client(new_client)
    return updated_client.getClientJSON()

@router.post("/", tags=["client"], dependencies=[Depends(verifyTokenEmployee)])
async def create_client(client: dict[str, str], token: str = Depends(verifyToken)) -> dict[str, str]:
    """
    Create a new client
    """     
    print("Client creation requested")
    CompanyName = client["CompanyName"]
    CIF = client["CIF"]
    address = client["address"]
    email = client["email"]
    phone = client["phone"]
    contact = client["contact"]
    
    new_client = Client( CompanyName=CompanyName, CIF=int(CIF), address=address, email=email, phone=int(phone), contact=contact)
    
    # Verify the client
    if not new_client.ready_to_insert():
        print("Client verification failed")
        raise HTTPException(status_code=400, detail="Client verification failed, missing fields")
    
    # Create the client
    created_client = clientDAO.create_client(new_client)
    return created_client.getClientJSON()