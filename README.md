# ElasticSearch Database of the MAG dataset
This module contains functions that sends `GET` requests to the ElasticSearch database of the Microsoft Academic Graph data built in the `Osprey1` server of the University of Illinois at Urbana-Champaign. Also, functions that fetches search result from Google Scholar is served as a benchmark system.
* All indexes correspond to an entity with the same name in the MAG dataset from Azure, except that ```author_oag``` index contains MAG author data from [OAG](https://www.microsoft.com/en-us/research/project/open-academic-graph/). Please refer to [Microsoft Academic Graph data schema](https://docs.microsoft.com/en-us/academic-services/graph/reference-data-schema) for details of indexes.
* 
## Setup
* Log in to the University's server ```Osprey1.csl.illinois.edu```.
* Clone the repository to the server.
* Run ```pip install -r src/requirements.txt```
* Open Kibana dashboard in a browser using http://128.174.136.27:5601/app/home#/, and interact with the REST API of ElasticSearch in `Dev Tools`.

```
ElasticSearch-MAG-Database
    - config/ 
        -- Elasticsearch/
          --- elasticsearch.yml
        -- Kibana/
          --- kibana.yml
        -- Logstash/
          --- logstash_author.conf
          --- logstash_affil.conf
          --- logstash_paper_author.conf
          --- logstash_paper.conf
          --- logstash_paper_reference.conf
          --- logstash_json.conf 
    - src/
        -- chromedriver
        -- query.py
        -- requirements.txt
        -- scholar.py
        -- scraper.py
```
* ```config/``` contains configuration files used for ElaticSearch, Kibana and Logstash.
* ```src/query.py``` defined the class ```es_helper``` that is connected to the ElasticSearch database and supports making search query to the database or perform cross index search, e.g. search for all papers published by an author given the author's name and author's affiliation. 
* ```src/scholar.py```compares the result of query from ElasticSearch and that from Google Scholar to verify the performance.
* ```src/scraper.py``` scrapes for the full form of an academic institution given its acronym in [Wikepedia](https://en.wikipedia.org/wiki/Main_Page). 
## Author
Jiaqi Cao
