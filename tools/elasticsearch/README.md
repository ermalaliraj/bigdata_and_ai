# elasticsearch spring-boot

### Running

1. Run `elasticsearch server` in local and make sure [http://localhost:9200/_cat/indices](http://localhost:9200/_cat/indices) replies.
2. Run the app `ElasticSearchApplication.java`
3. Use the following endpoints in POSTMAN for testing the app.

### Add
```
POST http://localhost:9200/api/person
{
    "id": "2",
    "name": "Ermal"
}
```

### Search 
```
http://localhost:9200/api/person/_search?        => all
http://localhost:9200/api/person/uE1A1H0BlwKbDa5NtRZD  => by id
```

### Other calls
```
http://localhost:9200/_aliases
http://localhost:9200/_cat/indices?h=index
http://localhost:9200/person?ignore_throttled=false&ignore_unavailable=false&expand_wildcards=open%2Cclosed&allow_no_indices=false
```

### SQL workbench
```
SHOW TABLES;
SHOW FUNCTIONS;

DESCRIBE person;
SELECT * from person;
SHOW COLUMNS from person;
```

http://localhost:9200/_aliases
http://localhost:9200/_cat/indices?
http://localhost:9200/_cat/indices?h=index
http://localhost:9200/person/_delete_by_query


### Links 
* [Elasticsearch SQL](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-spec.html)
* [Elasticsearch spring-boot video](https://www.youtube.com/watch?v=IiZZAu2Qtp0)


