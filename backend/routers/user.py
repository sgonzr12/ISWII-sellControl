from fastapi import Depends, APIRouter
from backend.verificator import verifyToken
 

from DAO.employeDAO import EmployeDAO 
        
# App user related endpoints

router = APIRouter()

employeDAO = EmployeDAO()


@router.get("/", tags=["user"], dependencies=[Depends(verifyToken)])
async def get_user(token: dict[str,str] = Depends(verifyToken)) -> dict[str,str]:
    """
    Get user information
    """
    print ("User info requested")# TODO: REMOVE WHEN LOGGER IS READY


    user = employeDAO.retriveOrCreate(token["sub"], token["name"], token["family_name"], token["email"])

    return user.getUserJSON()

