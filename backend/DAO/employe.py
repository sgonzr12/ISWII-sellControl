class Employe:
    
    roles = {
        "none":0,
        "admin":1,
        "manager":2,
        "sales":3,
        "warehousemanager":4,
        
    }
    def __init__(self, employe_id: str, name: str, family_name: str, email: str, rol: int):
        self.employe_id = employe_id
        self.name = name
        self.family_name = family_name
        self.email = email
        
        if 0 <= rol <= 6:
            self.rol = rol
        else:
            raise ValueError("rol must be between 1 and 6")

    def __repr__(self):
        return f"Employee(employeeID={self.employe_id}, rol={self.rol})"
    
    def getUserJSON(self) -> dict[str, str]:
        """
        Get user information as a JSON object
        """
        return {
            "employe_id": str(self.employe_id),
            "name": self.name,
            "family_name": self.family_name,
            "email": self.email,
            "rol": str(self.rol)
        } 