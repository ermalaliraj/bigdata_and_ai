# Download EU Law from EUR-lex

Open source project on how to download law from `EUR-lex`. 
All the present content is taken from the official page [wwww.eur-lex.europa.eu](https://eur-lex.europa.eu) and the 
source code has been created following the website guidelines. The code is open source and compliant with 
[Decision 2011/833/EU](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32011D0833).

### Publications Office
`Publications Office` of the European Union is the official provider of publishing services to all EU institutions, bodies, and agencies. 
It is a central point of access to EU law, publications, open data, research results and other official information.

### Official Journal
The `Official Journal` of the European Union (OJ) is the official publication for EU legal acts, published by the `Publications Office` of the EU.
For example Regulation nr.1304 of 2013 can be consulted here: [https://eur-lex.europa.eu/eli/reg/2013/1304/oj](https://eur-lex.europa.eu/eli/reg/2013/1304/oj) 

### ELI - European Legislation Identifier
ELI uniquely identifies a legislation online to access, exchange and reuse a Legislation.

### What is EUR-Lex?
`EUR-Lex` provides the official access to EU legal documents. 
It contains documents such as EU treaties, EU legislation and case-law from the EU Court of Justice.
It is available in all of the EU’s 24 official languages and is updated daily.
It contains electronic versions of all Official Journals since the first edition.

### Who runs EUR-Lex?
EUR-Lex is run by the `Publications Office` of the EU.

### Cellar 
The `Publications Office's` common repository for access to EU law and publications based on `semantic technology`.

|   | RSS notifications | Metadata | Metadata and content|
|---|---|---|---|
| EUR-Lex (meant for humans) | Custom |  Web services | EUR-Lex website |
| Cellar (meant for machines) | Full |  Sparql endpoint | RESTful interface |

Cellar SPARQL endpoint: [http://publications.europa.eu/webapi/rdf/sparql](http://publications.europa.eu/webapi/rdf/sparql)
Query: 
```
PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> SELECT * where {?s ?p ?o} limit 100
```

### Find an Act in Cellar  
1) Search for reg/2013/1303 `http://data.europa.eu/eli/reg/2013/1303/oj` in the SPARQL database and get its directUrl.
```
PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
SELECT DISTINCT  ?manifestation
WHERE
  { ?work  cdm:resource_legal_eli  ?eli
FILTER ( ?eli = "http://data.europa.eu/eli/reg/2021/467/oj"^^<http://www.w3.org/2001/XMLSchema#anyURI> )
    ?work ^cdm:expression_belongs_to_work ?expression .
    ?expression  cdm:expression_uses_language  ?lng
FILTER ( ?lng = <http://publications.europa.eu/resource/authority/language/ENG> )
    ?manifestation cdm:manifestation_manifests_expression  ?expression ;
    cdm:manifestation_type  ?type
FILTER regex(str(?type), "fmx4")
  }
```
Response:
``` 
{  "head": {"link": [], "vars": ["manifestation"]},
  "results": {
    "distinct": false, "ordered": true, "bindings": [ {"manresource_legal_eliifestation": { "type": "uri",
          "value": "http://publications.europa.eu/resource/cellar/fcd9e6d2-6c02-11e3-9afb-01aa75ed71a1.0006.02"
        }}]}
}
```
Use the postfix `/zip` do download the full Act or `/DOC_2` for the Legal Text. Examples:
[http://publications.europa.eu/resource/cellar/fcd9e6d2-6c02-11e3-9afb-01aa75ed71a1.0006.02/DOC_2](http://publications.europa.eu/resource/cellar/fcd9e6d2-6c02-11e3-9afb-01aa75ed71a1.0006.02/DOC_2)
[http://publications.europa.eu/resource/cellar/fcd9e6d2-6c02-11e3-9afb-01aa75ed71a1.0006.02/zip](http://publications.europa.eu/resource/cellar/fcd9e6d2-6c02-11e3-9afb-01aa75ed71a1.0006.02/zip)
[http://publications.europa.eu/resource/cellar/c6b2f374-231f-47e0-a846-d23b9375af12.0003.01](http://publications.europa.eu/resource/cellar/c6b2f374-231f-47e0-a846-d23b9375af12.0003.01)
 
 
### Get documents in Official Journal
```
PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
SELECT distinct ?OJ ?title_ group_concat(distinct ?author; separator=",") as ?authors ?date_document ?manif_fmx4 ?fmx4_to_download
WHERE 
{
	?work a cdm:official-journal.
	?work cdm:work_date_document ?date_document.
	FILTER(substr(str(?date_document),1,4)='2019')
	?work cdm:work_created_by_agent ?author.
	?work owl:sameAs ?OJ.
	FILTER(regex(str(?OJ),'/oj/'))
	OPTIONAL{?exp cdm:expression_title ?title.
		?exp cdm:expression_uses_language ?lang.
		?exp cdm:expression_belongs_to_work ?work.
		FILTER(?lang =<http://publications.europa.eu/resource/authority/language/ENG>)
		OPTIONAL{?manif_fmx4 cdm:manifestation_manifests_expression ?exp.
			?manif_fmx4 cdm:manifestation_type ?type_fmx4.
			FILTER(str(?type_fmx4)='fmx4')
		}
	}
	BIND(IF(BOUND(?title),?title,'The Official Journal does not exist in that language'@en) as ?title_)
	BIND(IF(BOUND(?manif_fmx4),IRI(concat(?manif_fmx4,"/zip")),"") as ?fmx4_to_download)
} order by ?date_document
limit 100
```

### Get all ELI resources  (REG)

```
PREFIX  owl:  <http://www.w3.org/2002/07/owl#>
PREFIX  cdm:  <http://publications.europa.eu/ontology/cdm#>

SELECT DISTINCT  substr(str(?OJ), 52, 3) substr(str(?OJ), 58, 4) ?OJ ?date_document ?fmx4_act
WHERE
  { ?work  cdm:resource_legal_eli  ?eli ;
           cdm:work_date_document  ?date_document
    FILTER regex(str(?eli), "/reg/")
    FILTER ( substr(str(?date_document), 1, 4) IN ("2016") )
    ?work  owl:sameAs  ?OJ
    FILTER regex(str(?OJ), "/oj/")
    OPTIONAL
      { ?exp  cdm:expression_title  ?title ;
              cdm:expression_uses_language  ?lang ;
              cdm:expression_belongs_to_work  ?work
        FILTER ( ?lang = <http://publications.europa.eu/resource/authority/language/ENG> )
        OPTIONAL
          { ?manif_fmx4  cdm:manifestation_manifests_expression  ?exp ;
                      cdm:manifestation_type  ?type_fmx4
            FILTER ( str(?type_fmx4) = "fmx4" )
            BIND(strlen(?exp) AS ?len_o)
          }
      }
    FILTER ( ?len_o != 0 )
    BIND(if(bound(?manif_fmx4), iri(concat(?manif_fmx4, "/DOC_2")), "") AS ?fmx4_act)
  }
```

 
### Links 
- [EUR-lex](https://eur-lex.europa.eu/content/welcome/about.html)
- [Official Journal](https://eur-lex.europa.eu/content/help/oj/about-oj.html)
- [Official Journal e-learning](https://eur-lex.europa.eu/content/e-learning/official_journal.html)
- [How to reuse EUR-Lex content](https://eur-lex.europa.eu/content/help/data-reuse/reuse-contents-eurlex-details.html)
- [DataExtractionUsingWebServices pdf](https://eur-lex.europa.eu/content/tools/webservices/DataExtractionUsingWebServices-v1.00.pdf)
- [External EUR-LEX integration BuhlRasmussen.eu](http://api.epdb.eu/)
- [CELLAR pdf](https://op.europa.eu/en/publication-detail/-/publication/658088eb-c071-11e8-9893-01aa75ed71a1/language-en/format-PDF/source-76875949)
- [OJ per years](https://data.europa.eu/data/datasets?keywords=oj-c-information&locale=en&dataScope=eu&country=eu&format=CSV&page=1&sort=release_date%2Bdesc)
- [OJ per years 2021](https://data.europa.eu/data/datasets/official-journals-of-the-european-union-2021?locale=en)
- [About ELI](https://eur-lex.europa.eu/eli-register/about.html)
- [ELI technical informations](https://eur-lex.europa.eu/eli-register/technical_information.html)
- [ELI - Video](https://www.youtube.com/watch?v=3ngoIDyuKMQ)
- [Document reg/2013/1303 from OJ](./resources/reg_2013_1303_oj.xml)
- [Document reg/2013/1303 in AkomaNtoso format](./resources/reg_2013_1303_akn.xml)
###
- [Back to bigdata_and_ai](https://github.com/ermalaliraj/bigdata_and_ai) 