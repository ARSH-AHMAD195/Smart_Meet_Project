from datetime import datetime, timedelta
import calendar

def parse_due_date_natural(text):
    today = datetime.now()
    text = text.lower().strip()

    if text == "today":
        return today.date()

    # Parse weekday names like "wednesday"
    weekdays = list(calendar.day_name)  # ["Monday", "Tuesday", ...]
    weekdays_lower = [d.lower() for d in weekdays]

    # "Wednesday"
    if text in weekdays_lower:
        target = weekdays_lower.index(text)
        delta = (target - today.weekday() + 7) % 7
        return (today + timedelta(days=delta)).date()

    # "Thursday next week"
    if "next week" in text:
        name = text.replace("next week", "").strip()
        if name in weekdays_lower:
            target = weekdays_lower.index(name)
            # jump to next week's target weekday
            delta = ((7 - today.weekday()) + target) + 7
            return (today + timedelta(days=delta)).date()

    return None

# due_date = "Today"
# print(parse_due_date_natural(due_date))