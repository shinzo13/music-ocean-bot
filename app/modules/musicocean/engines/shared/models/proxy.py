from pydantic import BaseModel


class Proxy(BaseModel):
    type: str
    address: str
    port: int
    login: str
    password: str
