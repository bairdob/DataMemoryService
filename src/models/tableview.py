from pydantic import BaseModel


class TableView(BaseModel):
    offset: int
    limit: int
