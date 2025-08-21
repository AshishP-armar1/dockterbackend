from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from models.user import SlotDay, Appointment
from schemas.request_response import BookAppointmentRequest, AppointmentResponse
from core.db import get_db
from utils.jwt_token import get_current_user  # assuming you already have JWT auth
import json

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("/book", response_model=AppointmentResponse)
def book_slot(
    req: BookAppointmentRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    # Check slot day exists
    slot_day = db.query(SlotDay).filter(SlotDay.date == req.date).first()
    if not slot_day:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No slots available for {req.date}",
        )

    # Convert slots JSON into dict
    slots_data = slot_day.slots

    # Check if slot exists
    if req.slot_time not in slots_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Slot {req.slot_time} not available",
        )

    # Check if already booked
    if slots_data[req.slot_time] == "booked":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Slot {req.slot_time} is already booked",
        )

    # Mark slot as booked
    print(slots_data)
    slots_data[req.slot_time] = "booked"
    print("after slot data",slots_data)
    slot_day.slots = slots_data

    
    db.add(slot_day)
    # Create appointment
    appointment = Appointment(
        date=req.date,
        slot_time=req.slot_time,
        issue=req.issue,
        age=req.age,
        gender=req.gender,
        issue_duration=req.issue_duration,
        user_id=current_user.id,
    )

    db.add(appointment)
    db.commit()
    slots_data[req.slot_time] = "booked"
    slot_day.slots = slots_data 
    print(slots_data)
    db.commit()
    db.refresh(appointment)

    return appointment
