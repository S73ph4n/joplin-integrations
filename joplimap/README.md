# JoplIMAP.py
Sync your IMAP Inbox with Joplin.

## Usage
Install requirements:
```bash
pip install -r requirements.txt
```

Run the script:
```bash
python joplimap.py
```

## With Docker (recommended)
```sh
docker build -t joplimap https://github.com/S73ph4n/joplin-integrations.git\#:joplimap
docker run -it --network host -e JOPLIN_TOKEN="myJoplinToken1a2b3c..." -e IMAP_SERVER="imap.myserver.com" -e IMAP_USER="username" -e IMAP_PASSWORD="password" joplimap
```

or with docker-compose :

```yaml
services:
  joplimap:
    build: https://github.com/S73ph4n/joplin-integrations.git\#:joplimap
    environment:
      - JOPLIN_TOKEN=myJoplinToken1a2b3c...
      - IMAP_SERVER=imap.myserver.com
      - IMAP_USER=testuser
      - IMAP_PASSWORD=testpassword
    network_mode: host
    restart: unless-stopped
```

## Configuration
All the variables which this script asks for (JOPLIN\_TOKEN, IMAP\_HOST, etc.) can be set from environment variables.

### Options
* JOPLIN\_TOKEN (**required**): the key to the Joplin Web Clipper API, see Joplin Options
* JOPLIN\_HOST (optionnal, default: localhost)
* JOPLIN\_PORT (optionnal, default: 41184)
* NOTES\_TAG (optionnal, default: email): the tag to apply to the notes
* IMAP\_SERVER (**required**)
* IMAP\_USER (**required**)
* IMAP\_PASSWORD (**required**)
* WAIT\_TIME (optionnal, default: 60): how long to wait between two runs
