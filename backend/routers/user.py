from fastapi import Depends, APIRouter
import logging

from verificator import verifyToken, verifyTokenAdmin

from DAO.employeDAO import EmployeDAO 
        
# App user related endpoints

router = APIRouter()
employeDAO = EmployeDAO()

@router.get("/", tags=["user"], dependencies=[Depends(verifyToken)])
async def get_user(token: dict[str,str] = Depends(verifyToken)) -> dict[str,str]:
    """
    Get user information
    """
    logging.debug("User information requested")
    # print the token
    logging.debug(f"Token: {token}")
    
    # if there is no field "family_name" in the token, set it to ""
    if "family_name" not in token:
        token["family_name"] = ""

    user = employeDAO.retriveOrCreate(token["sub"], token["name"], token["family_name"], token["email"])
    logging.info(f"User {user.getUserJSON()} retrieved")
    return user.getUserJSON()

@router.get("/users", tags=["user"], dependencies=[Depends(verifyTokenAdmin)])
async def get_all_users() -> list[dict[str,str]]:
    """
    Get all users information
    """
    logging.debug("Information of all users requested")
    users = employeDAO.get_all_employees()
    users_json = [user.getUserJSON() for user in users]

    logging.info(f"Information of {len(users)} users retrieved")
    return users_json


@router.put("/update", tags=["user"], dependencies=[Depends(verifyTokenAdmin)])
async def update_user(employeData: dict[str,str]) -> dict[str,str]:
    """
    Update user information
    """
    logging.debug("User information update requested")

    employe_id = employeData["employe_id"]
    rol = int(employeData["rol"])
    
    if rol < 0 or rol > 4:
        logging.debug("Invalid rol value")
        raise ValueError("rol must be between 0 and 6")
    
    employe = employeDAO.get_employee_by_id(employe_id)
    employe = employeDAO.update_employee(employe_id, employe.name, employe.family_name, employe.email, rol)

    logging.info(f"User {employe_id} updated")
    return employe.getUserJSON()        
