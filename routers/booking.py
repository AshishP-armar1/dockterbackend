from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from core.db import get_db
from models.user import SlotDay
from schemas.request_response import SlotsResponse
from utils.jwt_token import get_current_user

router = APIRouter(prefix="/slots", tags=["Slots"])


# Predefined slots for a day
DEFAULT_SLOTS = {
    "10:00": "unbooked",
    "10:20": "unbooked",
    "10:40": "unbooked",
    "11:00": "unbooked",
    "11:30": "unbooked",
}

#
@router.get("/view/{date}",response_model=SlotsResponse )
def view_slots(
    date: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    View slots for a given date.
    If slots don't exist → create default ones.
    """

    try:
        # Convert string to date object
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    # Check if slots exist for given date
    slot_day = db.query(SlotDay).filter(SlotDay.date == date_obj).first()

    if not slot_day:
        # Create default slot structure
        slot_day = SlotDay(date=date_obj, slots=DEFAULT_SLOTS)
        db.add(slot_day)
        db.commit()
        db.refresh(slot_day)
    
    print(slot_day.slots)
    return slot_day



