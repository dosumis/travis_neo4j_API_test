import requests
import json
import warnings

"""Add typing via anonymous class expressions from OWL file.
Requires uniqueness constraint on individual & class short_form_id."""


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]
        
def commit_list(cypher_statments, base_uri, usr, pwd):
    """Commit a list of statements to neo4J DB via REST API.
    Prints requests status and warnings if any problems with commit.
    cypher_statments = list of cypher statements as strings
    base_uri = base URL for neo4J DB.
    Returns"""
    
    ## This is designed for cypher statments that write to the DB, 
    # not for statements that return data to be processed.  It could be
    # Extended to deal with this. Easiest approach would be to just return whole result.
    statements = []
#   results = {}
    for s in cypher_statments:
        statements.append({'statement': s})
    payload = {'statements': statements}
    response = requests.post(url = "%s/db/data/transaction/commit" % base_uri, auth = (usr, pwd) , data = json.dumps(payload))
    if rest_return_check(response):
        return True
#       results.(response.json()['results'])
    else:
        return False
    
def commit_list_in_chunks(cypher_statments, base_uri, usr, pwd, chunk_length=100):
    """Commit a list of statements to neo4J DB via REST API, split into chunks.
    cypher_statments = list of cypher statements as strings
    base_uri = base URL for neo4J DB
    Default chunk size = 100 statements. This can be overidden by KWARG chunk_length
    """
    chunked_statements = chunks(l = cypher_statments, n=chunk_length)
    for c in chunked_statements:
        commit_list(c, base_uri, usr, pwd)
    
def rest_return_check(response):
    """Checks status response to post. Prints warnings to STDERR if not OK.
    If OK, checks for errors in response. Prints any present as warnings to STDERR.
    Returns True STATUS OK and no errors, otherwise returns False.
    """
    if not (response.status_code == 200):
        warnings.warn("Connection error: %s (%s)" % (response.status_code, response.reason))
    else:
        j = response.json()
        if j['errors']:
            for e in j['errors']:
                warnings.warn(str(e))
            return False
        else:
            return True
        
                
        
    
    