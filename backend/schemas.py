from pydantic import BaseModel

class ApplicationBase(BaseModel):
    first_name: str
    last_name: str
    address: str
    expected_salary: int

class ApplicationCreate(ApplicationBase):
    pass

class Application(ApplicationBase):
    id: int

    class Config:
        orm_mode = True
