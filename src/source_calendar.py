# for the google api
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
from os import path

import datetime

# The ID of the calendar to be scraped
CAL_ID = "<calendar id>"


def getLessons(first_day, last_day):
    """
    Returns a list of strings from the descriptions of events from the first day of the month to
    the last. Only evens with "Lesson' in their summary and descriptions other than 'None' are
    considered.
    @params first_day The first day of the month
    @params last_day The last day of the month
    """
    calendar_creds = path.expanduser("<full path to google calendar credentials .json file>")
    # Gives readonly permissions to this scrape
    scope = "https://www.googleapis.com/auth/calendar.readonly"
    credentials = ServiceAccountCredentials.from_json_keyfile_name(calendar_creds, scope)
    # "Builds" the calendar
    service = discovery.build("calendar", "v3", credentials=credentials)
    # Gets all the events in the month (among) other things
    events_result = (
        service.events()
        .list(
            calendarId=CAL_ID,
            timeMin=first_day,
            timeMax=last_day,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    # Gets only the events in the month
    events = events_result.get("items", [])
    # A list os strings of the lesson's descriptions
    lesson_descriptions = []

    if not events:
        print("No upcoming events found.")
    for event in events:
        summary = event.get("summary")
        if "Lesson" in summary:
            description = event.get("description")
            total = f"{description}"
            if total != "None":
                lesson_descriptions.append(total)
    return lesson_descriptions
