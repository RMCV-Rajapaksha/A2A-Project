import random
from datetime import date, datetime, timedelta

from google.adk.agents import LlmAgent

def generate_lakmina_meeting_calendar() -> dict[str, list[str]]:
    """Generates a random meeting availability calendar for Lakmina for the next 7 days."""
    calendar = {}
    today = date.today()
    possible_times = [f"{h:02}:00" for h in range(8, 21)]  # 8 AM to 8 PM

    for i in range(7):
        current_date = today + timedelta(days=i)
        date_str = current_date.strftime("%Y-%m-%d")
        available_slots = sorted(random.sample(possible_times, 8))
        calendar[date_str] = available_slots

    print("Lakmina's meeting calendar:", calendar)
    return calendar

LAKMINA_MEETING_CALENDAR = generate_lakmina_meeting_calendar()

def get_lakmina_meeting_availability(start_date: str, end_date: str) -> str:
    """
    Checks Lakmina's availability for meetings for a given date range.

    Args:
        start_date: The start of the date range to check, in YYYY-MM-DD format.
        end_date: The end of the date range to check, in YYYY-MM-DD format.

    Returns:
        A string listing Lakmina's available times for meetings in that date range.
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()

        if start > end:
            return "Invalid date range. The start date cannot be after the end date."

        results = []
        delta = end - start
        for i in range(delta.days + 1):
            day = start + timedelta(days=i)
            date_str = day.strftime("%Y-%m-%d")
            available_slots = LAKMINA_MEETING_CALENDAR.get(date_str, [])
            if available_slots:
                availability = f"On {date_str}, Lakmina is available for meetings at: {', '.join(available_slots)}."
                results.append(availability)
            else:
                results.append(f"Lakmina is not available for meetings on {date_str}.")

        return "\n".join(results)

    except ValueError:
        return (
            "Invalid date format. Please use YYYY-MM-DD for both start and end dates."
        )

def create_agent() -> LlmAgent:
    """Constructs the ADK agent for Lakmina for meeting scheduling."""
    return LlmAgent(
        model="gemini-2.0-flash",
        name="Lakmina_Agent",
        instruction="""
            **Role:** You are Lakmina's meeting scheduling assistant at Inter.
            Your sole responsibility is to manage Lakmina's meeting calendar and respond to inquiries 
            about her availability for meetings.

            **Core Directives:**

            *   **Check Availability:** Use the `get_lakmina_meeting_availability` tool to determine 
                    if Lakmina is free on a requested date or over a range of dates. 
                    The tool requires a `start_date` and `end_date`. If the user only provides 
                    a single date, use that date for both the start and end.
            *   **Polite and Concise:** Always be polite and to the point in your responses.
            *   **Stick to Your Role:** Do not engage in any conversation outside of scheduling. 
                    If asked other questions, politely state that you can only help with scheduling meetings.
        """,
        tools=[get_lakmina_meeting_availability],
    )