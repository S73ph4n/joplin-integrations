"""JoplIMAP.py : a script to fetch your email and continuously import it to Joplin."""
import os
import time
import click
from imap_tools import MailBox, AND  # TODO : use imaplib ?
import python_joplin
from python_joplin import tools
import logging

logger = logging.getLogger("jop_logger")

CONFIRM = False  # ask before creating each note/ressource
LOOP = True

# Environment variables we need:
ENV = {
    "JOPLIN_TOKEN": "",
    "JOPLIN_HOST": "localhost",
    "JOPLIN_PORT": "41184",
    "NOTES_TAG": "email",
    "IMAP_SERVER": "",
    "IMAP_USER": "",
    "IMAP_PASSWORD": "",
    "WAIT_TIME": "60",
}


def format_str(raw):
    """Format a string so it doesn't break the Joplin API calls (happens with some characters)."""
    forbidden_chars = ["\n", "\r", "#", "\\", "'", '"']
    return "".join([c for c in raw if not c in forbidden_chars])
    # return(''.join([c for c in raw if c.isalnum() or c.isspace()]))
    # return(''.join([c for c in raw if c.isprintable()]))


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
        inbox_notebook = jop.get_notebook_by_title(
            "IMAP_Inbox", create_if_needed=True
        )  # get the Joplin notebook we need
        click.echo("Joplin connection OK")

        # Prepare IMAP-Tools:
        click.echo("Connecting to IMAP server...")
        mb = MailBox(ENV["IMAP_SERVER"]).login(
            ENV["IMAP_USER"], ENV["IMAP_PASSWORD"], initial_folder="INBOX"
        )  # Connect to IMAP server
        click.echo("IMAP connection OK.\nFetching messages...")
        # messages = mb.fetch(criteria=AND(seen=False), mark_seen=False, bulk=True)  # get unread messages
        messages = mb.fetch(mark_seen=False, bulk=True)  # get all messages
        click.echo("Messages fetched.")

        # Process the messages:
        # ( See https://pypi.org/project/imap-tools/#email-attributes )
        for msg in messages:
            if not CONFIRM or click.confirm(
                "Add message " + msg.subject + " ?", default=False
            ):
                # title = msg.date_str + " : " + format_str(msg.subject) + " [" + msg.from_ + "]"
                title = (
                    msg.date.strftime("[%Y-%m-%d %H:%M:%S]")
                    + " "
                    + format_str(msg.subject)
                    + " ["
                    + msg.from_
                    + "]"
                )
                note = inbox_notebook.get_note_by_title(
                    title, create_if_needed=True, allow_external_results=True
                )  # Create note in notebook (or find it if it exists)
                if note.body != "":
                    continue  # if there's already something, let's not change it
                # note.body = markdownify.markdownify(msg.html, heading_style='ATX') #doesn't work
                tools.set_yaml(note, "From", msg.from_)
                tools.set_yaml(note, "To", ",".join(msg.to))
                tools.set_yaml(note, "Cc", ",".join(msg.cc))
                tools.set_yaml(note, "Bcc", ",".join(msg.bcc))
                note.body += "\n" + msg.text
                for att in msg.attachments:
                    if not CONFIRM or click.confirm(
                        "\tAdd attachment " + att.filename + " ?", default=True
                    ):
                        att_jop = jop.new_ressource(att.filename, att.payload)
                        note.body += "[" + att_jop.title + "](:/" + att_jop.id + ")"
                note.source = "Email via JoplIMAP"
                note.add_tag_by_title(ENV["NOTES_TAG"], create_if_needed=True)
                note.push()  # Push updates to Joplin

    except Exception:
        logger.exception("Fatal error in main loop")

    if not LOOP:
        break
    click.echo("Done. Waiting " + str(ENV["WAIT_TIME"]) + " secs before next run...")
    time.sleep(int(ENV["WAIT_TIME"]))
