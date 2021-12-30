# ElasticSearch Database of the MAG dataset
This module contains functions that sends `GET` requests to the Elasticsearch database of the Microsoft Academic Graph data built in the `Osprey1` server of the University of Illinois at Urbana-Champaign. Google Scholar is served as a benchmark system through functions that fetches search result from Google Scholar and compares that from the database. Also, this module supports search for acronyms through a scraper that scrapes for the [Wikipedia](https://en.wikipedia.org/wiki/Main_Page)'s result for the most likely institutions the acronyms refer to.
## About the database
* All indexes correspond to an entity with the same name in the MAG dataset from Azure. Please refer to [Microsoft Academic Graph data schema](https://docs.microsoft.com/en-us/academic-services/graph/reference-data-schema) for details of indexes.
* [A placeholder for index management page in the Kibana interface]
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
        -- full_form_detector.py
        -- data/
            --- R1R2_research_college_cs_faculty.csv
```
* ```config/``` contains configuration files used for Elaticsearch, Kibana and Logstash.
* ```src/query.py``` defined the class ```es_helper``` that is connected to the Elasticsearch database and supports making search query to the database or perform cross index search, e.g. search for all papers published by an author given the author's name and author's affiliation. 
* ```src/scholar.py```compares the result of query from ElasticSearch and that from Google Scholar to verify the performance.
* ```src/full_form_detector.py``` scrapes for the full form of an academic institution given its acronym in Wikipedia. 
## Usage
* ``````
## Built with
This module uses the following open source packages:
* [Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
* [Kibana](https://www.elastic.co/guide/en/kibana/current/index.html)
* [Logstash](https://www.elastic.co/guide/en/logstash/current/index.html)
* [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/#)
## Author
Jiaqi Cao
