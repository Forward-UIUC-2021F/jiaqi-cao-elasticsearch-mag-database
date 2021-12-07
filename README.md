# ElasticSearch Database of MAG dataset
## Description
An database of the Microsoft Academic Graph dataset is constructed with ElasticSearch and the ELK Stack. 
* ```src/query.py``` defined the class ```es_helper``` that is connected to the ElasticSearch database and supports making search query to the database or perform cross index search, e.g. search for all papers published by an author given the author's name and author's affiliation. 
* ```src/scholar.py```compares the result of query from ElasticSearch and that from Google Scholar to verify the performance.
* ```config``` contains configuration files used for ElaticSearch, Kibana and Logstash.
* Please refer to [Microsoft Academic Graph data schema](https://docs.microsoft.com/en-us/academic-services/graph/reference-data-schema) for details of the database.
## Getting Started
* Log in to the University's server ```Osprey1.csl.illinois.edu```.
* Clone the repository to the server.
* Run ```pip install -r src/requirements.txt```
* Open Kibana dashboard in a browser http://128.174.136.27:5601/app/home#/
## Author
Jiaqi Cao
