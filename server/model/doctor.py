from enum import unique
from server.database import Base
from sqlalchemy import Column,Integer,String, ForeignKey
from sqlalchemy.orm import relationship
class Doctorregistration(Base):
    __tablename__ = 'doctorregistration'
    id  = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    email = Column(String, unique=True)
    mobile = Column(String)
    sector = Column(String)
    location = Column(String)
    address = Column(String)
    qualification = Column(String)
    fees= Column(String)
    image = Column(String)
    password = Column(String)
class appointment(Base):
    __tablename__ = 'appointment'
    
    id = Column(Integer, primary_key=True)
    date = Column(String)
    day = Column(String)
    slots = relationship("slot",primaryjoin="appointment.id == slot.appointment_id",cascade="all, delete-orphan")
    
class slot(Base): 
    __tablename__ = 'slot'
    
    id = Column(Integer, primary_key=True)
    slot = Column(String)
    slot_book_doctor = Column(String)
    appointment_id = Column(Integer, ForeignKey('appointment.id'),nullable=False)
        
class patientregistration(Base):
    __tablename__ ='patientregistration'
    
    id= Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    mobile = Column(String, unique=True)
    address = Column(String)
    pincode = Column(Integer)  