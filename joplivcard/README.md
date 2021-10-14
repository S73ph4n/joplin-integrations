# JopliVCard.py
Sync your contacts with Joplin.

Looks for notes' dates and build a VCard file from it.
## Usage
Install requirements:
```bash
pip install -r requirements.txt
```

Run the script:
```bash
python joplivcard.py
```

## With Docker (recommended)
```sh
docker build -t joplivcard https://github.com/S73ph4n/joplin-integrations.git\#:joplivcard
docker run -it --network host -e JOPLIN_TOKEN="myJoplinToken1a2b3c..." -v ./joplivcard_files:/data joplivcard
```

or with docker-compose (recommended):

```yaml
services:
  joplivcard:
    build: https://github.com/S73ph4n/joplin-integrations\#:joplivcard
    environment:
      - JOPLIN_TOKEN=myJoplinToken1a2b3c...
    volumes:
      - ./joplivcard_files:/data
    network_mode: host
```

## Configuration
All the variables which this script asks for (JOPLIN\_TOKEN) can be set from environment variables.

### Options
* JOPLIN\_TOKEN (**required**): the key to the Joplin Web Clipper API, see Joplin Options
* JOPLIN\_HOST (optionnal, default: localhost)
* JOPLIN\_PORT (optionnal, default: 41184)
* WAIT\_TIME (optionnal, default: 60): how long to wait between two runs

## Serving the VCard file
TODO
