from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Body
from server.database import SessionLocal
from fastapi import Depends
from sqlalchemy.orm import Session
from server.controller.doctor import CryptContext
import base64
import uuid
import datetime
import calendar

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


from server.controller.doctor import(
    get_doctor,
    add_doctor,
    update_doctor_data, 
    get_doctor_by_id,
    add_appionmentdata,
    get_appoiment_id,
    get_appionment_by_id,
    add_slot,
    get_slot_by_id,
    get_all_slot,
    add_patient,
    get_patient_id,
    patient_data
)

from server.model.schema import(
    Requestdoctorschema,
    Requestupdatedoctorschema,
    RequestDoctorlogin,
    Requestappointment,
    Requestslotschema,
    Requestdemoschema,
    Requestpatientschema
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
async def create_doctor(request: Requestdoctorschema, db: Session = Depends(get_db)):
    try:
        await add_doctor(db, doctordata = request.parameter)
        return {"status":"Ok","code":200,"message":"Doctor created successfully"}
    except Exception as e:
        return {"Message": e.args, "code" :500}

@router.get("/")
async def get_books( db: Session = Depends(get_db)):
    doctordata = get_doctor(db)
    return  {'status':"Ok",'code':"200",'message':"All data show Sucessfully",'msg':doctordata}


@router.put("/update/{doctorregistration_id}")
async def update_doctor_data_by_id( doctorregistration_id : int, request : Requestupdatedoctorschema,db: Session = Depends(get_db)):
    try:
        data = jsonable_encoder(request)
        update_doctor = update_doctor_data(db, doctorregistration_id , **data.get('parameter'))
        return  {'status':"Ok",'code':200,"Message": "Doctor profie updated successfully.", "Data": update_doctor}
    except Exception as e:
        return {"Message" : e.args , "code":500}


@router.get("/getdata/{doctorregistration_id}")
async def getby_id(doctorregistration_id: int, db: Session = Depends(get_db)):    
    usersdata = get_doctor_by_id(db, doctorregistration_id= doctorregistration_id)
    if usersdata is None:
        return {"Msg" : "No doctor registered"}
    return {"Message" : usersdata}


@router.delete("/delete/{doctorregistration_id}")
async def delete_doctor_data( doctorregistration_id : int, db: Session = Depends(get_db)):
    try: 

        db.delete(get_doctor_by_id(db, doctorregistration_id= doctorregistration_id))
        db.commit()

        return {'status':"Ok",'code':"200",'message':"Doctor Data delete successfully"}
    except Exception as e:
        return {"Message" : e.args}
    
@router.post("/doctorlogin")
async def doctor_login( request: RequestDoctorlogin, db: Session = Depends(get_db)):
    try:
        data = jsonable_encoder(request)
        doctor =await doctor_login(db, data.get('parameter').get('email'))
        if pwd_context.verify(data.get('parameter').get('password'), doctor.password):
            return {"status":"Ok","code":200,"message":"Doctor login successfully", "msg":"Hiii"}
        else:
            return {"status":"Error","code":400,"message":"Invalid password", "msg": "fcrvghj"}
    except Exception as e:
        return {"status":"Error","code":500,"message": e.args}
    


async def cheak_date(date):
    born =  datetime.datetime.strptime(date, '%d %m %Y').weekday()
    return calendar.day_name[born]

@router.post("/cheakholiday")
async def cheakholiday (request :str ):
    '''
    request=  03-08-2022
    '''
    try:
        date = " ".join(request.split("-"))
        born =  await cheak_date(date)
        return {"Code":200,"Message":born}
        
    except Exception as e:
        return {"Message":e.args, "Code":500}
    
@router.post("/Appionments_Create")
async def create_appionment(reqest : Requestappointment, db = Depends(get_db)):
    try:
        data = jsonable_encoder(reqest)
        date= data['parameter']['date']
        date = " ".join(date.split("-"))
        day = await cheak_date(date)
        if day == "Sunday":
            return{"Message":"It is holiday time"}
        else  :
            data['parameter']['day']= day  
            await add_appionmentdata (db, appionmentdata = data['parameter'])
            return {"Message":"ok"}
    except Exception as e:
        return {"Message" : e.args, "Code":500}
    
@router.get("/getdata/{appionment_id}")
async def getby_id(appionment_id: int, db: Session = Depends(get_db)):    
    try:
        data_appionment= get_appionment_by_id(db, appionment_id= appionment_id)
        if data_appionment is None:
            return {"Message" : f"ID {appionment_id} No Registered"}
        return {"Message" : data_appionment}
    except  Exception as e: 
        return {"Message" : e.args}     

@router.post("/addslot")
async def addslot(request : Requestdemoschema ,  db= Depends(get_db)):
    try:
        data = jsonable_encoder(request)
        booking =data['parameter']['slot']
        date = data['parameter']['date']
        appionment_id = await get_appoiment_id(db,ap_date=date)
        appionment_ids=list(appionment_id)
        i=0
        for j in appionment_ids:
            i=int(getattr(j,"id"))
        book_slot = await get_all_slot(db, id=i)
        if booking in book_slot:
            return{"Message": "slot already booked"}
        else :
            add_data={}
            add_data["appointment_id"]=i
            add_data["slot"]=booking
            add_data["slot_book_doctor"]="string"
            add_slot(db, slotdata = add_data)
            return{"Message":"Slot Sucessfully Book",  "Code": 200 ,"Result": add_data}
    except Exception as e:
        return {"Message" : e.args, "Code":500} 

@router.get("slot_show_by_id/{appionment_id}")
async def slot_show(appionment_id : int,db =Depends(get_db)):
    try:
        data_slot = get_slot_by_id(db, ids=appionment_id)
        if data_slot is None:
            return {"Message" :f"Id {appionment_id} No Registered"}
        data_slot=list(data_slot) 
        return {"Message" :list(data_slot)}
    except Exception as e:
        return {"Message" :e.args, "Code":500}


@router.get("get_slot_by_date/{date}")
async def get_slot_by_date(date: str ,db = Depends(get_db)) :
    try: 
        date_slot = await get_appoiment_id(db,date)
        date_slot = list(date_slot)
        for j in date_slot :
            appointment_id=(getattr(j,"id"))
            slot= await get_all_slot(db,id=appointment_id)
            data ={
                'date_slot':date_slot,
                'slot':slot
            }
            return {"Message": data}
        return {"Message" :f" {date} Slot Not Available"}
    except Exception as e:  
        return {"Message" :e.args, "Code":500}
    
@router.post("/patientregistration")
async def add_patient_data(request : Requestpatientschema, db= Depends(get_db)):
    try:
        await add_patient (db, patientdata =request.parameter)
        return {"Status":"Ok", "code":200,"Message":"Patient added successfully"}
    except Exception as e:
        return {"Message":e.args, "code" : 500}   
    
@router.get("/patient/{patients_id}")
async def patient_id(patients_id : int, db :Session =Depends(get_db)):
    try:
        data_patient =await get_patient_id(db , patient_id= patients_id)
        if data_patient is None:
            return {"Message": f"patient {patients_id} does not found"}
    except Exception as e:
        return {"Message" : e.args, "Code":500}
        
@router.get("/add_patient_data")
async def all_patient_data(db :Session =Depends(get_db)):
    data = await patient_data(db)
    return {"Status": "Ok","Code":200, "Message":"All patient data Show","Data":data}
