# NIFI & ELK on Docker

Run the latest version of our NIFI & ELK stack on Docker

## Requirements

### Host setup

* [Docker Engine](https://docs.docker.com/install/) version **17.05** or newer
* [Docker Compose](https://docs.docker.com/compose/install/) version **1.20.0** or newer
* 2 GB of RAM

By default, the stack exposes the following ports:

* 5044: Logstash Beats input
* 5000: Logstash TCP input
* 9600: Logstash monitoring API
* 9200: Elasticsearch HTTP
* 9201: Elasticsearch TCP transport
* 5601: Kibana

## Docker Setup
Run the following command in this folder:
```docker compose up```

## NIFI Setup
The test files are already in "\Docker-NIFI-ELK\nifi\flowfile_repository\nifi_input" folder but will be deleted after the first time the Nifi pipeline is run. Please make sure to create a copy of it on your local machine for more than one run. Copying and pasting the local copy of the test files into the nifi_input folder will be enough to set up the Nifi pipeline before running it.

## ELK Setup
For the first time we run ELK, we will need to create index patterns. This has to be done after the Nifi workflow has been run at least once. To create the index patterns,
1. Go to "Stack Management-\>Kibana-\>Index Patterns" and click "Create index pattern". 
2. Type "tikac\*" into the box for "Index pattern name" and click "Next step". 
3. Click "file.creationTime" for the "Time field" box and click "Create index pattern"
4. Repeat steps one to three, using "tikam\*" for the "Index pattern name" box
