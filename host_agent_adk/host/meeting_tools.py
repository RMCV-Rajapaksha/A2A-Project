from datetime import date, datetime, timedelta
from typing import Dict


# In-memory database for meeting room schedules, mapping date to a dictionary of time slots and company names
MEETING_ROOM_SCHEDULE: Dict[str, Dict[str, str]] = {}


def generate_meeting_room_schedule():
    """Generates a schedule for the meeting room for the next 7 days."""
    global MEETING_ROOM_SCHEDULE
    today = date.today()
    possible_times = [f"{h:02}:00" for h in range(8, 21)]  # 8 AM to 8 PM

    for i in range(7):
        current_date = today + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")
        MEETING_ROOM_SCHEDULE[date_str] = {time: "unknown" for time in possible_times}

# Initialize the schedule when the module is loaded
generate_meeting_room_schedule()


def list_meeting_room_availabilities(date: str) -> dict:
    """
    Lists the available and booked time slots for a meeting room on a given date.

    Args:
        date: The date to check, in YYYY-MM-DD format.

    Returns:
        A dictionary with the status and the detailed schedule for the day.
    """
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return {
            "status": "error",
            "message": "Invalid date format. Please use YYYY-MM-DD.",
        }

    daily_schedule = MEETING_ROOM_SCHEDULE.get(date)
    if not daily_schedule:
        return {
            "status": "success",
            "message": f"The meeting room is not open on {date}.",
            "schedule": {},
        }

    available_slots = [
        time for time, company in daily_schedule.items() if company == "unknown"
    ]
    booked_slots = {
        time: company for time, company in daily_schedule.items() if company != "unknown"
    }

    return {
        "status": "success",
        "message": f"Schedule for {date}.",
        "available_slots": available_slots,
        "booked_slots": booked_slots,
    }


def book_meeting_room(
    date: str, start_time: str, end_time: str, reservation_name: str
) -> dict:
    """
    Books a meeting room for a specified date and time range under a reservation name.

    Args:
        date: The date to book, in YYYY-MM-DD format.
        start_time: Start time in HH:MM format.
        end_time: End time in HH:MM format.
        reservation_name: Name of the company or group reserving the room.

    Returns:
        A dictionary with the status and a message.
    """
    try:
        start_dt = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")
    except ValueError:
        return {
            "status": "error",
            "message": "Invalid date or time format. Please use YYYY-MM-DD and HH:MM.",
        }

    if start_dt >= end_dt:
        return {"status": "error", "message": "Start time must be before end time."}

    if date not in MEETING_ROOM_SCHEDULE:
        return {"status": "error", "message": f"The meeting room is not open on {date}."}

    if not reservation_name:
        return {
            "status": "error",
            "message": "Cannot book a meeting room without a reservation name.",
        }

    required_slots = []
    current_time = start_dt
    while current_time < end_dt:
        required_slots.append(current_time.strftime("%H:%M"))
        current_time += timedelta(hours=1)

    daily_schedule = MEETING_ROOM_SCHEDULE.get(date, {})
    for slot in required_slots:
        if daily_schedule.get(slot, "booked") != "unknown":
            company = daily_schedule.get(slot)
            return {
                "status": "error",
                "message": f"The time slot {slot} on {date} is already booked by {company}.",
            }

    for slot in required_slots:
        MEETING_ROOM_SCHEDULE[date][slot] = reservation_name

    return {
        "status": "success",
        "message": f"Success! The meeting room has been booked for {reservation_name} from {start_time} to {end_time} on {date}.",
    }