from fastapi import APIRouter, HTTPException, Body
from typing import List
from app.database import models
from app.database import engine, SessionLocal
from app.database import schemas

# models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

router = APIRouter(
    tags=["Point"],
    responses={404: {"description": "Not found"}},
)


@router.get('/user/{user_id}', description="Get user info with total points by <user_id>")
def get_user(user_id: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(404)
    return schemas.User.from_orm(user)


@router.post('/user', response_model=schemas.User)
def create_user(user: schemas.UserCreate = Body(...)):
    new_user = models.User(username=user.username)
    db.add(new_user)
    db.commit()
    return schemas.User.from_orm(new_user)


@router.post('/point/receive', response_model=schemas.PointRecord)
def receive_point(record: schemas.CreatePointReceivedRecord = Body(...)):
    new_record = models.PointRecords(**record.dict())
    update_user = db.query(models.User).filter(models.User.id == record.user_id).first()
    if not update_user:
        raise HTTPException(404)
    update_user.total_points += record.transaction_points
    db.add(new_record)
    db.add(update_user)
    db.commit()
    return schemas.PointRecord.from_orm(new_record)


@router.post('/point/consume', response_model=schemas.PointRecord)
def consume_point(record: schemas.CreatePointConsumedRecord = Body(...)):
    # Here should have logics for verifying if consumed points is the correct amount by <consumed_package_id>.
    # If not, raise 400 as bad request
    new_record = models.PointRecords(**record.dict())
    update_user = db.query(models.User).filter(models.User.id == record.user_id).first()
    if not update_user:
        raise HTTPException(404)
    update_user.total_points -= record.transaction_points
    db.add_all([new_record, update_user])
    db.commit()
    return schemas.PointRecord.from_orm(new_record)


@router.get('/point/records/{user_id}', response_model=List[schemas.PointRecord])
def get_user_point_records(user_id: str):
    cursor = db.query(models.PointRecords)\
        .filter(models.PointRecords.user_id == user_id)\
        .order_by(models.PointRecords.timestamp.desc()).all()
    return [schemas.PointRecord.from_orm(c) for c in cursor]
