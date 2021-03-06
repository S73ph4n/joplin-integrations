"""JoplICAL : sync an ICalendar with your notes."""
import os
import time
import click
import re
from icalendar import Calendar, Event
import python_joplin
from python_joplin import tools
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("jop_logger")

CONFIRM = False  # ask before creating each note/ressource
LOOP = True

# Environment variables we need:
ENV = {
    "JOPLIN_TOKEN": "",
    "JOPLIN_HOST": "localhost",
    "JOPLIN_PORT": "41184",
    "WAIT_TIME": "60",
    "NOTES_TAG": "",
    "MODE": "todo, body",
}

# Date format (ISO only for now)
date_regex = re.compile(
    "[0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}\:[0-9]{2}"
)  # matches dates
date_format = "%Y-%m-%d %H:%M"  # for datetime.strptime

MODE = ENV["MODE"].replace(" ", "").split(",")


def get_dates(note):
    """Extract all dates related to a note.
    Returns a list of datetime."""
    dates = []
    if note.todo_due != 0 and "todo" in MODE:  # if it has a due date:
        dates.append(tools.format_date(note.todo_due))
    if "body" in MODE:
        dates_in_body = date_regex.findall(note.body)
        for d_i_b in dates_in_body:  # if it has date(s) in the body of the note:
            dates.append(datetime.strptime(d_i_b, date_format))
    return dates


# In case the environment variables are not set, let's set them :
for VAR_NAME in ENV.keys():
    if not os.getenv(VAR_NAME):
        if CONFIRM:
            ENV[VAR_NAME] = click.prompt(
                "Enter your " + VAR_NAME, type=str, default=ENV[VAR_NAME]
            )
    else:
        ENV[VAR_NAME] = os.getenv(VAR_NAME)
        click.echo(VAR_NAME + " found in the environment.")

while True:
    try:
        # Prepare Joplin:
        click.echo("Connecting to Joplin...")
        jop = python_joplin.Joplin(
            ENV["JOPLIN_TOKEN"], host=ENV["JOPLIN_HOST"], port=int(ENV["JOPLIN_PORT"])
        )  # Connect to the Joplin API
        click.echo("Joplin connection OK")
        click.echo("Fetching notes...")
        if ENV["NOTES_TAG"] != "":
            tag = jop.get_tag_by_title(ENV["NOTES_TAG"])
            notes = tag.get_notes()  # Get only the notes tagged
        else:
            notes = jop.get_notes()  # Get all the notes
        click.echo("Notes fetched.")

        # Prepare calendar:
        cal = Calendar()
        cal["summary"] = "Joplin Calendar"

        # Process the notes:
        for note in notes:
            if not CONFIRM or click.confirm(
                "Add note " + note.title + " ?", default=False
            ):
                for note_date in get_dates(note):
                    event = Event()
                    event.add("summary", note.title)
                    event.add("description", note.body)
                    # TODO : add Joplin share link
                    event.add("dtstart", note_date)
                    duration = tools.get_yaml(note, "duration")
                    if duration:
                        event.add("duration", timedelta(hours=float(duration)))
                    else:
                        event.add("duration", timedelta(hours=1))  # Lasts 1 hour
                    # TODO : get YAML properties
                    cal.add_component(event)

        # Saving calendar:
        f = open("/data/joplin_cal.ics", "wb")
        f.write(cal.to_ical())
        f.close()

    except Exception:
        logger.exception("Fatal error in main loop")

    if not LOOP:
        break
    click.echo("Done. Waiting " + str(ENV["WAIT_TIME"]) + " secs before next run...")
    time.sleep(int(ENV["WAIT_TIME"]))
