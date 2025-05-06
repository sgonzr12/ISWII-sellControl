from fastapi import Depends, APIRouter
from app import verifyToken

from DAO.employeDAO import EmployeDAO 
from connect import get_db_connection
        
# App user related endpoints

router = APIRouter()

employeDAO = EmployeDAO(get_db_connection())


@router.get("/", tags=["user"], dependencies=[Depends(verifyToken)])
async def get_user(token: dict[str,str] = Depends(verifyToken)) -> dict[str,str]:
    """
    Get user information
    """
    print ("User info requested")# TODO: REMOVE WHEN LOGGER IS READY


    user = employeDAO.retriveOrCreate(int(token["sub"]), token["name"], token["family_name"], token["email"])

    return user.getUserJSON()

