from pydantic import BaseModel


class HealthCheckSchema(BaseModel):
    status: str
    API_users: str
    API_visitas: str
    API_equipamentos: str
