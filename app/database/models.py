from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from . import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=uuid4)
    username = Column(String(36), nullable=False)
    total_points = Column(Integer, default=0)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # point_received_records = relationship("PointReceivedRecords")
    # point_consumed_records = relationship("PointConsumedRecords")
    point_records = relationship("PointRecords")


class PointRecords(Base):
    __tablename__ = "point_records"
    record_id = Column(String(36), primary_key=True, default=uuid4)
    user_id = Column(String(36), ForeignKey("users.id"), index=True)
    timestamp = Column(DateTime, default=datetime.now)
    transaction_points = Column(Integer)
    point_source_id = Column(String(36), nullable=True)
    consumed_package_id = Column(String(36), nullable=True)
    user = relationship("User", back_populates="point_records")

#
# class PointReceivedRecords(Base):
#     __tablename__ = "point_received_records"
#
#     received_id = Column(String(36), primary_key=True, default=uuid4)
#     user_id = Column(String(36), ForeignKey("users.id"), index=True)
#     received_time = Column(DateTime, default=datetime.now)
#     received_points = Column(Integer)
#     point_source_id = Column(String(36))
#
#     user = relationship("User", back_populates="point_received_records")
#
#
# class PointConsumedRecords(Base):
#     __tablename__ = "point_consumed_records"
#
#     consumed_id = Column(String(36), primary_key=True, default=uuid4)
#     user_id = Column(String(36), ForeignKey("users.id"), index=True)
#     consumed_time = Column(DateTime, default=datetime.now)
#     consumed_points = Column(Integer)
#
#     user = relationship("User", back_populates="point_consumed_records")