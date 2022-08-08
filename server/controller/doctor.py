from sqlalchemy.orm import Session
from server.model.doctor import Doctorregistration, appointment, slot , patientregistration
from server.model.schema import DoctorSchema, Requestslotschema, patientschema 
from passlib.context import CryptContext

from server.utils.image_hendler import image_upload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_doctor(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Doctorregistration).offset(skip).limit(limit).all()

def get_doctor_by_id(db: Session, doctorregistration_id: int):
    return db.query(Doctorregistration).filter(Doctorregistration.id == doctorregistration_id).first()

async def add_doctor(db: Session, doctordata : DoctorSchema ):

    
    img_path=await image_upload(doctordata.image)
    
    doctor = Doctorregistration(name=doctordata.name, 
                                username=doctordata.username,
                                email = doctordata.email,
                                mobile = doctordata.mobile,
                                sector = doctordata.sector,
                                location = doctordata.location,
                                address = doctordata.address, 
                                qualification = doctordata.qualification,
                                fees = doctordata.fees, 
                                image= img_path,
                                password =  pwd_context.hash(doctordata.password))
    db.add(doctor)  
    db.commit()
    db.refresh(doctor)
    return doctor


def update_doctor_data(db: Session, doctorregistration_id : int,name: str, username : str, email : str, mobile : int, sector : str, location : str ,
                       address :str, qualification : str,fees : str, image: str):
    doctor = get_doctor_by_id(db=db, doctorregistration_id=doctorregistration_id)
    
    doctor.name=name 
    doctor.username=username,
    doctor.email = email,
    doctor.mobile = mobile,
    doctor.sector = sector,
    doctor.location = location,
    doctor.address = address, 
    doctor.qualification = qualification,
    doctor.fees = fees, 
    doctor.image= image,

    db.commit()
    db.refresh(doctor)
    return doctor

def doctor_login(db: Session, loginemail:str ):
    return db.query(Doctorregistration).filter(Doctorregistration.email == loginemail).first()

async def add_appionmentdata(db: Session, appionmentdata: dict):
    
    data = appointment(
        date=appionmentdata["date"],
        day=appionmentdata["day"],
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


async def get_appionment_by_id(db: Session, appionment_id: int):
    return db.query(appointment).filter(appointment.id == appionment_id).first()


async def add_slot(db: Session, slotdata: Requestslotschema):

    data = slot(
        appointment_id=slotdata["appointment_id"],
        slot=slotdata["slot"],
        slot_book_doctor=slotdata["slot_book_doctor"],
    )

    db.add(data)
    db.commit()
    db.refresh(data)
    return data


async def get_slot_by_id(db: Session, ids):
    return db.query(slot).filter(slot.appointment_id == int(ids))


async def get_appoiment_id(db: Session, ap_date):
    data_slot = db.query(appointment).filter(appointment.date == str(ap_date))
    return data_slot


async def get_all_slot(db: Session, id):
    data_slot = db.query(slot).filter(slot.appointment_id == int(id))
    data_slot = list(data_slot)
    book_slots = []
    for j in data_slot:
        book_slots.append(getattr(j, "slot"))
    return book_slots


async def data_slot(db: Session):
    date_all = db.query(appointment).filter(appointment.date)
    print(date_all)

async def add_patient(db: Session, patientdata :patientschema):

    patient = patientregistration(name=patientdata.name, 
                                email = patientdata.email,
                                mobile = patientdata.mobile,
                                address = patientdata.address,
                                pincode = patientdata.pincode)
    db.add(patient)  
    db.commit()
    db.refresh(patient)
    return patient

async def get_patient_id(db :Session , patient_id :int):
    return db.query(patientregistration).filter(patientregistration.id == patient_id).first()

async def patient_data(db :Session):
    return db.query(patientregistration).all()