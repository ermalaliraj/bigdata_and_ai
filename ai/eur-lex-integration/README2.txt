# Download EU Laws from EUR-Lex (EU Official Journal)


### What is EUR-Lex?
`EUR-Lex` provides the official access to EU legal documents. 
It contains documents such as EU treaties, EU legislation and case-law from the EU Court of Justice.
It is available in all of the EU’s 24 official languages and is updated daily.

### Who runs EUR-Lex?
EUR-Lex is run by the `Publications Office` of the European Union which is the official provider of publishing services
to all EU institutions, bodies, and agencies. 
It is a central point of access to EU law, publications, open data, research results and other official information.
https://eur-lex.europa.eu/content/e-learning/official_journal.html

### Official Journal
The `Official Journal` of the European Union (OJ) is the official publication for EU legal acts, published by 
the `Publications Office` of the EU.
EUR-Lex contains electronic versions of all Official Journals since the first edition.

The Official Journal of the European Union (OJ) is composed of 2 series:
- `L` Legislation
- `C` Information and notices (C stands for French 'communications').

Celex number
`Celex number` is the unique identifier of each document in EUR-lex. 
It do not change depending on the language of the document.
Example: `3 2003 L 0112`  or `3 2003 L 0112 2018072017`
- `3` Legislation Document
- `2003` year
- `L` Directive
- `0112` DocNr
- `2018072017` date of entry into force of hte latest amendment, when more than one version.

### Cellar 
The `Publications Office's` common repository for access to EU law and publications based on `semantic technology`.

|   | RSS notifications | Metadata | Metadata and content|
|---|---|---|---|
| EUR-Lex (meant for humans) | Custom |  Web services | EUR-Lex website |
| Cellar (meant for machines) | Full |  Sparql endpoint | RESTful interface |

Cellar endpoint `http://publications.europa.eu/webapi/rdf/sparql`
SPARQL: 
```
PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> SELECT * where {?s ?p ?o} limit 100
```

### ELI - European Legislation identifier
uniquely identifies a legislation online.
 
### Content 
- [EUR-lex](https://eur-lex.europa.eu/content/welcome/about.html)
- [Official Journal](https://eur-lex.europa.eu/content/help/oj/about-oj.html)
- [Official Journal e-learning](https://eur-lex.europa.eu/content/e-learning/official_journal.html)
- [How to reuse EUR-Lex content](https://eur-lex.europa.eu/content/help/data-reuse/reuse-contents-eurlex-details.html)
- [ELI - European Legislation identifier](https://www.youtube.com/watch?v=3ngoIDyuKMQ)



## How?

- url: 
    - http://publications.europa.eu/webapi/rdf/sparql  
- eli vocabulary CMD
    - http://publications.europa.eu/resource/cellar/eacea2d9-fd33-11e8-a96d-01aa75ed71a1.0001.01/DOC_2
    - http://publications.europa.eu/resource/cellar/427fb40c-2d9e-11eb-b27b-01aa75ed71a1.0001.02/DOC_1#d4e19707
-  eur-lex information
    - https://eur-lex.europa.eu/eli-register/technical_information.html 
    
###   SPARQL Query for OJ


### Call OJ


# GET Formex document
- [Publications europa.eu reg/2013/1303](http://publications.europa.eu/resource/cellar/fcd9e6d2-6c02-11e3-9afb-01aa75ed71a1.0006.02/DOC_2)
- [Document reg/2013/1303 from OJ](./resources/reg_2013_1303_oj.xml)
- [Document reg/2013/1303 in AkomaNtoso format](./resources/reg_2013_1303_akn.xml)
- [European Official Journey](https://eur-lex.europa.eu/advanced-search-form.html?action=update&qid=1623662226455) - All document are taken from OJ
- [Back to bigdata_and_ai](https://github.com/ermalaliraj/bigdata_and_ai)

- [api.epdb.eu](http://api.epdb.eu/)
(https://op.europa.eu/en/publication-detail/-/publication/658088eb-c071-11e8-9893-01aa75ed71a1/language-en/format-PDF/source-76875949)


- [Reuse eur-lex data](https://eur-lex.europa.eu/content/help/data-reuse/reuse-contents-eurlex-details.html)
- [OJ per years](https://data.europa.eu/data/datasets?keywords=oj-c-information&locale=en&dataScope=eu&country=eu&format=CSV&page=1&sort=release_date%2Bdesc)


https://eur-lex.europa.eu/content/help/data-reuse/webservice.html
https://eur-lex.europa.eu/content/tools/webservices/DataExtractionUsingWebServices-v1.00.pdf


[What is EUR-Lex]
https://eur-lex.europa.eu/content/e-learning/what_is_eurlex.html
What is the EU legislation in force concerning the EuroVoc concept ‘climate change’?
```
prefix cdm: <http://publications.europa.eu/ontology/cdm#>

select distinct ?work
where
  { ?work cdm:resource_legal_in-force "true"^^<http://www.w3.org/2001/XMLSchema#boolean> ;
    a cdm:legislation_secondary;
    cdm:work_is_about_concept_eurovoc <http://eurovoc.europa.eu/5482> .
}
```


### Example What is the EU legislation in force concerning the EuroVoc concept ‘climate change’?
```
prefix cdm: <http://publications.europa.eu/ontology/cdm#>

select distinct ?work
where
  { ?work cdm:resource_legal_in-force "true"^^<http://www.w3.org/2001/XMLSchema#boolean> ;
    a cdm:legislation_secondary;
    cdm:work_is_about_concept_eurovoc <http://eurovoc.europa.eu/5482> .
}
```
