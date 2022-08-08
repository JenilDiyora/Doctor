from msilib.schema import File
from pydantic import BaseModel , Field
from pydantic.generics import GenericModel
from typing import Optional, TypeVar, Generic

T = TypeVar('T')

class DoctorSchema(BaseModel):
    name : Optional [str] = None
    username : Optional [str] = None 
    email : Optional [str] = None
    mobile : Optional [int] = None
    sector : Optional [str] = None
    location : Optional [str] = None
    address : Optional [str] = None
    qualification : Optional [str] = None
    fees : Optional [str] = None
    image : Optional [str] = None
    password : Optional [str] = None     
    
    class Config:
        orm_mode =True
    
class Requestdoctorschema(BaseModel):
    parameter: DoctorSchema = Field(...)
class Doctordataupdate(BaseModel):
    
    name : Optional [str] = None
    username : Optional [str] = None 
    mobile : Optional [int] = None
    sector : Optional [str] = None
    location : Optional [str] = None
    address : Optional [str] = None
    qualification : Optional [str] = None
    fees : Optional [str] = None
    image : Optional [str] = None
class Requestupdatedoctorschema(BaseModel):
    parameter: Doctordataupdate = Field(...)

class doctorlogin(BaseModel):
    
    email : Optional [str] = None
    password : Optional [str] = None

class RequestDoctorlogin(BaseModel):
    parameter : doctorlogin = Field (...)
     
class appointmentschema(BaseModel):
    
    date : Optional[str] = None
    class config :
        orm_mode = True
        
class Requestappointment(BaseModel):
    parameter : appointmentschema = Field(...)
    
class slotschema(BaseModel):
    
    appointment_id : Optional[int] =None
    slot :Optional[str] = None
    slot_book_doctor : Optional[str] = None
    
    class config :
        orm_mode = True
        
class Requestslotschema(BaseModel):
    parameter : slotschema = Field(...)
    
class demoschema(BaseModel):
    date : Optional[str] = None
    slot : Optional[str] = None
    
    class config :
        orm_mode =True

class Requestdemoschema(BaseModel):
    parameter: demoschema = Field(...)
    
class patientschema(BaseModel):
    
    name : Optional[str]
    email : Optional[str]    
    mobile : Optional[str]
    address : Optional[str]
    pincode : Optional[int]
    
    class config : 
        orm_mode = True
        
class Requestpatientschema(BaseModel):
    parameter : patientschema = Field(...)
class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)