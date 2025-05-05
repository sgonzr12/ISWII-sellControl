from fastapi import Depends
from app import verifyToken, verifyUser
from main import get_app

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

app = get_app();

@app.get("/user", tags=["user"], dependencies=[Depends(verifyToken), Depends(verifyUser)])
async def get_user(token: str = Depends(verifyToken)) -> dict[str,str]:
    """
    Get user information
    """
    user = User()
    return user.getUserJSON()

