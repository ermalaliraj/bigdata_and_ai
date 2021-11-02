# OJ

- url: 
    - http://publications.europa.eu/webapi/rdf/sparql  
- eli vocabulary CMD
    - http://publications.europa.eu/resource/cellar/eacea2d9-fd33-11e8-a96d-01aa75ed71a1.0001.01/DOC_2
    - http://publications.europa.eu/resource/cellar/427fb40c-2d9e-11eb-b27b-01aa75ed71a1.0001.02/DOC_1#d4e19707
-  eur-lex information
    - https://eur-lex.europa.eu/eli-register/technical_information.html 


###   SPARQL Query for OJ
```
PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>

SELECT DISTINCT  ?manifestation
WHERE
  { ?work  cdm:resource_legal_eli  ?eli 
    FILTER ( ?eli = "http://data.europa.eu/eli/reg/2013/1303/oj"^^<http://www.w3.org/2001/XMLSchema#anyURI> )
    ?work ^cdm:expression_belongs_to_work ?expression .
    ?expression  cdm:expression_uses_language  ?lng
	FILTER ( ?lng = <http://publications.europa.eu/resource/authority/language/ENG> )
    ?manifestation cdm:manifestation_manifests_expression  ?expression ;
    cdm:manifestation_type  ?type
	FILTER regex(str(?type), "fmx4")
  }
limit 100 
```

### Call OJ

```
QueryEngineHTTP qexec = QueryExecutionFactory.createServiceRequest(ojUrl, query);
ResultSet results = qexec.execSelect();
String json = new String(results...);
```

```
{
  "head": {
    "vars": [
      "manifestation"
    ]
  },
  "results": {
    "bindings": [
      {
        "manifestation": {
          "type": "uri",
          "value": "http://publications.europa.eu/resource/cellar/fcd9e6d2-6c02-11e3-9afb-01aa75ed71a1.0006.02"
        }
      }
    ]
  }
}
```

# GET Formex document
- [Publications europa.eu reg/2013/1303](http://publications.europa.eu/resource/cellar/fcd9e6d2-6c02-11e3-9afb-01aa75ed71a1.0006.02/DOC_2)
- [Document reg/2013/1303 from OJ](./resources/reg_2013_1303_oj.xml)
- [Document reg/2013/1303 in AkomaNtoso format](./resources/reg_2013_1303_akn.xml)
- [European Official Journey](https://eur-lex.europa.eu/advanced-search-form.html?action=update&qid=1623662226455) - All document are taken from OJ
- [Back to bigdata_and_ai](https://github.com/ermalaliraj/bigdata_and_ai)