from neo4j_tools import commit_list

statements = []
statements.append("CREATE (:Person { name: 'Romeo' } )")
statements.append("CREATE (:Person { name: 'Juliet' } )")
statements.append("MATCH (r:Person { name: 'Romero' } ), (j:Person { name: 'Juliet' }) MERGE (r)-[:Loves]-(j)")

base_uri = 'http://localhost:7474'
usr = 'neo4j'
pwd = ''
commit_list(statements, base_uri, usr, pwd)

