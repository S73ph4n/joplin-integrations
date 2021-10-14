"""JopliVCard : sync your contacts with your notes."""
import os
import time
import click
import re
import vobject
import python_joplin
from python_joplin import tools
from datetime import datetime, timedelta
import logging

logger = logging.getLogger('jop_logger')

CONFIRM = False  # ask before creating each note/ressource
LOOP = True

# Environment variables we need:
ENV = {"JOPLIN_TOKEN": "", "JOPLIN_HOST":"localhost", "JOPLIN_PORT":"41184", "WAIT_TIME":"60", "NOTES_TAG":"contact"}

vcards = ''

# In case the environment variables are not set, let's set them :
for VAR_NAME in ENV.keys():
    if not os.getenv(VAR_NAME):
        if CONFIRM:
            ENV[VAR_NAME] = click.prompt("Enter your " + VAR_NAME, type=str, default=ENV[VAR_NAME])
    else:
        ENV[VAR_NAME] = os.getenv(VAR_NAME)
        click.echo(VAR_NAME + " found in the environment.")

while True:
    try:
        # Prepare Joplin:
        click.echo("Connecting to Joplin...")
        jop = python_joplin.Joplin(ENV["JOPLIN_TOKEN"], host=ENV["JOPLIN_HOST"], port=int(ENV["JOPLIN_PORT"]))  # Connect to the Joplin API
        click.echo("Joplin connection OK")
        click.echo('Fetching notes...')
        if ENV["NOTES_TAG"] != "":
            tag = jop.get_tag_by_title(ENV["NOTES_TAG"])
            notes = tag.get_notes() #Get only the notes tagged
        else:
            notes = jop.get_notes() #Get all the notes
        click.echo('Notes fetched.')

        # Process the notes:
        for note in notes:
            if not CONFIRM or click.confirm(
                "Add note " + note.title + " ?", default=False
            ):
                j = vobject.vCard()

                #j.add('n')
                #j.n.value = vobject.vcard.Name( family='Harris', given='Jeffrey' )
                j.add('fn')
                j.fn.value = note.title

                categories = [t.title for t in note.tags].remove(ENV["NOTES_TAG"])
                categories.append('Joplin')
                j.add('categories')
                j.categories.value = categories

                j.add('note')
                j.note.value = note.body #TODO : de-markdown-ify

                tel = tools.get_yaml(note, 'tel')
                if tel:
                    j.add('tel')
                    j.tel.value = tel

                email = tools.get_yaml(note, 'email')
                if email:
                    j.add('email')
                    j.email.value = email
                    j.email.type_param = 'INTERNET'

                vcards += j.serialize()

        # Saving vcard:
        f = open('/data/joplin_vcards.vcf', 'w')
        f.write(vcards)
        f.close()

    except Exception:
        logger.exception("Fatal error in main loop")

    if not LOOP:
        break
    click.echo("Done. Waiting " + str(ENV["WAIT_TIME"]) + " secs before next run...")
    time.sleep(int(ENV["WAIT_TIME"]))
