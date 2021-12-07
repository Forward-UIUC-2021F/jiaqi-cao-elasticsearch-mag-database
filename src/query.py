from elasticsearch import Elasticsearch
import csv 
import re


class es_helper:
    def __init__(self):
        self.es = Elasticsearch([{'host': "0.0.0.0", 'port': 9200}])

    """
    results: result body from search

    returns: list of results in dictionary
    """
    def hits_processor(self, results):
        result_list = []
        hits = results["hits"]["hits"]

        if len(hits) != 0:
            for i in range(len(hits)):  
                print("result", i, ":")
                result = hits[i]["_source"]
                print(result)
                result_list.append(result)

        else:
            print("No hits found")

        return result_list
        
    """ 
    affil : string, name of affiliation
    size: int, number of result wanted to return

    returns: result body from elasticsearch whose displayed name matches affil
            that's parsed by hits_processor
    """

    def search_affiliation(self, affil : str, size = 1) -> list:
        print("searching for affiliation :", affil)

        body = {
                "bool": {
                    "must": [
                        {"match": {
                        "DisplayName": affil
                        }}
                    ]
                }
            }
        
        results = self.es.search(query = body, index = "affiliations", size = size)

        return self.hits_processor(results)

    """ 
    name : string, name of author
    size: int, number of result wanted to return

    returns: result body from elasticsearch whose displayed name matches author
            that's parsed by hits_processor
    """
    def search_author(self, name : str, size = 1) -> list:
        print("searching for affiliation :", name)

        body = {
                "bool": {
                    "must": [
                        {"match": {
                        "DisplayName": name
                        }}
                    ]
                }
            }
        results = self.es.search(query = body, index = "authors", size = size)

        return self.hits_processor(results)


    """ 
    paper_id: string, id of paper

    returns: result body from elasticsearch whose paper's id matches paper_id
    """

    def search_paper(self, paper_id: str, size =1) -> list():
        print("searching for paper id :", paper_id)

        body = {
                "bool": {
                    "must": [
                        {"match": {
                        "PaperId.keyword": paper_id
                        }}
                    ]}
            }
        results = self.es.search(query = body, index = "papers", size = size)

        return self.hits_processor(results)

    """ 
    name, affil: name and affiliation of the author

    returns: the first hit body as a dict in the result body from elasticsearch, else empty dict
    """
    def search_author_affiliation(self, name : str, affil : str, size = 1) -> list:
        print("searching for author : {} from {}".format(name, affil))

        affil_hits = self.search_affiliation(affil)

        if len(affil_hits):
            affil_id = affil_hits[0]["AffiliationId"]

            body = {"bool": {
                            "must": [
                                {"match": {
                                "DisplayName": name
                                }},
                                {
                                "match": {
                                    "LastKnownAffiliationId.keyword": affil_id
                                }
                                }
                            ]
                            }
                        }
            results = self.es.search(query = body, index = "authors", size = size)

            hits = self.hits_processor(results)
            print(type(hits))
            return hits

        else:
            print("Affiliation {} not found".format(affil))

        return dict()

     
    """ 
    name, affil(optional): name and affiliation of the author

    returns: the id of papers published by the author (from the papers_authors_affiliations index), else empty dict
    """
    def search_author_for_paperid(self, name : str, affil = "") -> list:
        print("searching for id of papers of author : {} from {}".format(name, affil))

        author_hits = self.search_author_affiliation(name, affil) if affil != "" else self.search_author(name)

        if len(author_hits):
            authorid = author_hits[0]["AuthorId"]
            size = author_hits[0]["PaperCount"]

            body = {"bool": {
                        "must": [
                            {"match": {
                            "AuthorId.keyword": authorid
                            }}
                        ]
                        }}
            results = self.es.search(query = body, size = size, index = "papers_authors_affiliations")

            hits = self.hits_processor(results)
            return hits
        else:
            return dict()


    """ 
    name, affil(optional): name and affiliation of the author
    sort_by: sort descendingly on the given feature (default publicated year)

    returns: the paper objects published by the queried author sorted
    """

    def search_author_for_paper(self, name : str, affil = "", sort_by = "Year") -> dict:
        print("searching for papers of author : {} from {}".format(name, affil))
        
        paperid_result = self.search_author_for_paperid(name, affil)
        hits = []
        if len(paperid_result):
            for row in paperid_result:
                paper_id = row["PaperId"]
                result = self.search_paper(paper_id)                
                hits += result

        return sorted(hits, key = lambda i: i['Year'], reverse = True)


"""
returns: list of [index, affiliation, name] lists of the CS faculty dataset
"""

def get_affil_author():

    with open("R1R2_research_college_cs_faculty.csv") as file:
        reader = csv.reader(file)
        uni_name = list(reader)
    print("successfully get",len(uni_name)," items")
    # first line is the heading 
    return uni_name[1:]


"""  
returns: list of [name, affil, hits from search_author_affiliation] lists of the CS faculty dataset
"""

def get_hit_list_faculty(name_idx = "authors", affil_index = "affiliations"):
    result_list = []
    affil_name = get_affil_author()
    es = es_helper()

    for _, affil, name in affil_name:
        hits = es.search_author_affiliation(name = name, affil = affil, name_idx = name_idx, affil_index = affil_index)
        result_list.append([name, affil, hits])

    return result_list

""" 
result_list: result returns from get_hit_list
file_name: the file that the result list stores to

returns: 
"""
def write_hits_to_file(result_list, file_name_csv = ""):
    valid_list = []
    authorid = []
    for result in result_list:    
        name, affil, data = result
        if len(data) != 0:
            valid_list.append(name + ";" + affil + ";" + str(data))
            authorid.append([name,affil,data["LastKnownAffiliationId"], data["AuthorId"]])
    with open(file_name_csv, "w") as csv_f:
        writer = csv.writer(csv_f)
        writer.writerow(["name", "affiliation", "LastKnownAffiliationId", "AuthorId"])
        writer.writerows(authorid)
    
    with open("author_id_with_data", "w") as f:
        for i in valid_list:
            f.write(i+"\n")
    
    print("successfully convert ", len(valid_list) ," items to file {}".format(file_name_csv))
    print("there are " , len(authorid) , " affiliation id")


if __name__ == "__main__":
    es = es_helper()
    
    # Modify this line for testing purposes
    print(len(es.search_author_for_paper(name = "abdussalam alawini", affil = "university of illinois at urbana champaign")))
    #print(es.search_author_for_paper(name = "Marty Banks", affil = "University of california Berkeley"))

    # Get result from searching CS faculties
    # print(get_hit_list_faculty())

    
    
    