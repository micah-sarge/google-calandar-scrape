import dest_spreadsheet
import source_calendar

import datetime


def main():
    """
    Calls the spreadsheet and calendar scripts to gather the lesson income of the previous month
    """
    today = datetime.datetime.now()
    datemax = datetime.datetime(today.year, today.month, 1, 23, 59, 59) - datetime.timedelta(days=1)
    # The last day of the previous month
    last_day = datemax.isoformat() + "Z"
    # If the current month is January, then December of last year is used. Otherwise, the
    # previous month is used
    dec = False
    if today.month != 1:
        first_day = datetime.datetime(today.year, today.month - 1, 1).isoformat() + "Z"
    else:
        first_day = datetime.datetime(today.year - 1, 12, 1).isoformat() + "Z"
        dec = True
    # Gets all the events with 'Lessons' in the title and not 'None' in the description
    lessons = source_calendar.getLessons(first_day, last_day)
    # Calculates the previous month's income and adds it to a google sheet
    if not dec:
        dest_spreadsheet.recordIncome(today.year, today.month - 1, lessons)
    else:
        dest_spreadsheet.recordIncome(today.year - 1, 12, lessons)


if __name__ == "__main__":
    main()
