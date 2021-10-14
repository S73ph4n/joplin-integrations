# JoplICal.py
Sync your calendar with Joplin.

Looks for notes' dates and build a iCalendar file (.ics) from it.
The following dates are used:
* The due date (for todos) of the todo note.
* Any occurence of a date formatted at YYYY-MM-DD HH:MM in the note's body.

Creates an event with the title as note's title and the description as the note's body.
## Usage
Install requirements:
```bash
pip install -r requirements.txt
```

Run the script:
```bash
python joplical.py
```

## With Docker (recommended)
```sh
docker build -t joplical https://github.com/S73ph4n/joplin-integrations.git\#:joplical
docker run -it --network host -e JOPLIN_TOKEN="myJoplinToken1a2b3c..." -v ./joplical_files:/data joplical
```

or with docker-compose (recommended):

```yaml
services:
  joplimap:
    build: https://github.com/S73ph4n/joplin-integrations\#:joplical
    environment:
      - JOPLIN_TOKEN=myJoplinToken1a2b3c...
    volumes:
      - ./joplical_files:/data
    network_mode: host
```

## Configuration
All the variables which this script asks for (JOPLIN\_TOKEN) can be set from environment variables.

### Options
* JOPLIN\_TOKEN (**required**): the key to the Joplin Web Clipper API, see Joplin Options
* JOPLIN\_HOST (optionnal, default: localhost)
* JOPLIN\_PORT (optionnal, default: 41184)
* WAIT\_TIME (optionnal, default: 60): how long to wait between two runs

## Serving the ICS file
This tool produces a .ics calendar file and keeps it up-to-date. To synchronize it to your devices, you might want to run a webserver, such as nginx:

WARNING: This is provided as a simple example of how to serve the file with Nginx. You should add some sort of authentifaction on top of this, since your calendar file contains information from your notes.

```yaml
services:
  joplimap:
    build: https://github.com/S73ph4n/joplin-integrations\#:joplical
    environment:
      - JOPLIN_TOKEN=myJoplinToken1a2b3c...
    volumes:
      - ./joplical_files:/data
    network_mode: host
  nginx:
    image: nginx
    ports:
      - 80:80
    volumes:
      - ./appdata/joplical:/usr/share/nginx/html
    environment:
      - PUID=1000
```

This serves your ICS file at ```http://localhost/joplin_cal.ics```. You can then use an app such as [ICSx5](https://icsx5.bitfire.at/) to synchronize your devices.

