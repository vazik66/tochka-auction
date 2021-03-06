from pydantic import BaseModel


class HealthCheck(BaseModel):
    db_connection: bool
    payment_api_working: bool
