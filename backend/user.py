from fastapi import Depends, APIRouter
from app import verifyToken, verifyUser
 

# Temporary user class for demonstration purposes. TODO: REMOVE WHEN DATABASE IS READY
class User:
    def __init__(self, name: str = "PEPE", userID: str = "123456"):
        self.name = name
        self.userID = userID
        self.rol = "6"
        
    def getUserJSON(self)-> dict[str,str]:
        return {
            "name": self.name,
            "userID": self.userID,
            "rol": self.rol
        }
        
        
        
# App user related endpoints

router = APIRouter()

@router.get("/", tags=["user"], dependencies=[Depends(verifyToken), Depends(verifyUser)])
async def get_user(token: str = Depends(verifyToken)) -> dict[str,str]:
    """
    Get user information
    """
    print ("User info requested")# TODO: REMOVE WHEN LOGGER IS READY
    user = User()
    return user.getUserJSON()

