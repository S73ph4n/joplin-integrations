# JoplIntegrate with a few things

Here are a few tools I use to integrate [Joplin](https://joplinapp.org/) with various other tools. They rely on my custom [Python Joplin library](https://github.com/S73ph4n/python_joplin).

They come without any warranties.

Currently, there is:
* JoplIMAP : pulls email from an IMAP server into a Joplin notebook
* JoplICal : makes a calendar from your notes and keeps it up-to-date
* JopliZot : pulls items from a Zotero library into a Joplin notebook

**More information on each tool can be found in the READMEs in their respective folders.**

## Installation
Make sure you have Joplin installed and that the Web Clipper API is active in Joplin options.

I strongly recommend you use Docker to build and run these tools.

I personnally use docker-compose with the following ```docker-compose.yml``` file :

(note: you have to fill in the environment variables left blank)

```docker-compose
services:
  joplimap:
    build: https://github.com/S73ph4n/joplin-integrations.git#:joplimap
    environment:
      - JOPLIN_TOKEN=
      - IMAP_SERVER=
      - IMAP_USER=
      - IMAP_PASSWORD=
    network_mode: host
  joplizot:
    build: https://github.com/S73ph4n/joplin-integrations.git#:joplizot
    environment:
      - JOPLIN_TOKEN=
      - ZOTERO_LIBRARY_ID=
      - ZOTERO_API_KEY=
      - ZOTERO_COLLECTION_ID=[optionnal]
    network_mode: host
  joplical:
    build: https://github.com/S73ph4n/joplin-integrations.git#:joplical
    environment:
      - JOPLIN_TOKEN=
    volumes:
      - ./appdata/joplical:/data
    network_mode: host
```


## Usage
You can then start the services with ```docker-compose up -d```.
If the environment variables have been set correctly, it should work without a hitch. Otherwise, use ```docker logs``` to identify what went wrong.

To stop it, run ```docker-compose down```.

## Contributing
These tools are far from perfect. If you encounter a bug, feel free to file an issue.

Pull requests welcome.

