from pydantic import BaseModel


class IngestSchema(BaseModel):
    status: str


class IngestErrorSchema(BaseModel):
    message: str
