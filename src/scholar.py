from scholarly import scholarly, ProxyGenerator    
from query import es_helper 
    
""" 
result from Google Scholar, serving as a benchmark system to compare with result returned from Elasticsearch

returns: a generator of publication objects
"""
def author_search(author = "", affiliation = "", year = ""):
    #pg = ProxyGenerator()
    #success = pg.FreeProxies()
    success = True
    if success:
        # scholarly.use_proxy(pg)
        """ 
        # search by Google scholar: profile
        search_query = scholarly.search_author(author+", "+affiliation) if affiliation != "" else scholarly.search_author(author)
        try:
            author = next(search_query)

            # Can add publication_limit below
            return scholarly.fill(author, sections = ["basic", "publications"])
        except:
            print("Author {} not found using scholarly".format(author, ",", affiliation))
            return dict() 
        """

        query = author + " " + affiliation + " " + year
        search_query = scholarly.search_pubs(query)
        return search_query
        
    else:
        print("Proxy not set up")
        return None


def compare_results(author = "", affiliation = "") -> bool:
    print("Comparing result of query: {}, {}".format(author, affiliation))
    
    es = es_helper()
    result_es = es.search_author_for_paper(author, affiliation)
    es_title = []

    if not len(result_es):
        print("author not found in MAG dataset")
        return False

    for result in result_es:
        es_title.append(result["PaperTitle"])


    result_scholar = author_search(author, affiliation, year = result_es[0]["Year"])
    while True:
        try:
            pub = next(result_scholar)
            title = pub["bib"]["title"].lower()
            if title in es_title:
                return True
        except:
            print("No match found from result returned by Google Scholar")
            return False
    
    return False

# Retrieve the author's data, fill-in, and print
# print(author_search("Marty Banks", "University of california Berkeley"))
#print(len(author_search("abdussalam alawini", "UIUC")['publications']))
print(compare_results("Marty Banks", "University of california Berkeley"))
# search_query = scholarly.search_pubs("martin banks university of California berkeley 2019")
# print(next(search_query))
# print(next(search_query))