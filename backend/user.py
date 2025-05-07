from fastapi import Depends, APIRouter
from app import verifyToken, verifyTokenAdmin

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

@router.get("/users", tags=["user"], dependencies=[Depends(verifyTokenAdmin)])
async def get_all_users() -> list[dict[str,str]]:
    """
    Get all users information
    """
    print ("All users info requested")
    users = employeDAO.get_all_employees()
    users_json = [user.getUserJSON() for user in users]
    return users_json


@router.put("/update", tags=["user"], dependencies=[Depends(verifyTokenAdmin)])
async def update_user(employe_id: str, rol: int) -> dict[str,str]:
    """
    Update user information
    """
    print ("User info updated")
    
    if rol < 0 or rol > 4:
        raise ValueError("rol must be between 0 and 6")
    
    employe = employeDAO.get_employee_by_id(employe_id)
    
    employe = employeDAO.update_employee(employe_id, employe.name, employe.family_name, employe.email, rol)
    
    return employe.getUserJSON()        
