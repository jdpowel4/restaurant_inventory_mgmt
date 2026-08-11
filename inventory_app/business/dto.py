from dataclasses import dataclass

@dataclass(frozen=True)
class BusinessInfo:
    name: str
    logo_path: str
    address: str 
    phone: str
    email: str