# JopliZot.py
Sync your Zotero library with Joplin.

## Usage
Install requirements:
```bash
pip install -r requirements.txt
```

Run the script:
```bash
python joplizot.py
```

## With Docker (recommended)
```sh
docker build -t joplizot https://github.com/S73ph4n/joplin-integrations.git\#:joplizot
docker run -it --network host -e JOPLIN_TOKEN="myJoplinToken1a2b3c..." -e ZOTERO_LIBRARY_ID=1234567 -e ZOTERO_API_KEY="myZotApiKey1a2b3c" joplizot
```

or with docker-compose :

```yaml
services:
  joplizot:
    build: https://github.com/S73ph4n/joplin-integrations.git\#:joplizot
    environment:
      - JOPLIN_TOKEN=myJoplinToken1a2b3c...
      - ZOTERO_LIBRARY_ID=1234567
      - ZOTERO_API_KEY=myZotApiKey1a2b3c...
    network_mode: host
    restart: unless-stopped
```

## Configuration
All the variables which this script asks for (JOPLIN\_TOKEN, ZOTERO\_LIBRARY\_ID, etc.) can be set from environment variables.

### Options
* JOPLIN\_TOKEN (**required**): the key to the Joplin Web Clipper API, see Joplin Options
* JOPLIN\_HOST (optionnal, default: localhost)
* JOPLIN\_PORT (optionnal, default: 41184)
* WAIT\_TIME (optionnal, default: 60): how long to wait between two runs
* ZOTERO\_LIBRARY\_ID (**required**)
* ZOTERO\_API\_KEY (**required**)
* ZOTERO\_COLLECTION\_ID (optionnal, by default fetches top-level items)
* NOTES\_TAG (optionnal, default: zotero): the tag to apply to the notes

### Zotero configuration
You do not need to have Zotero installed, but you need to have an account on Zotero.org. Then:
* Your ZOTERO\_LIBRARY\_ID can be found [here](https://www.zotero.org/settings/keys), under "Your userID for use in API calls".
* You must get your ZOTERO\_API\_KEY from [here](https://www.zotero.org/settings/keys/new)
