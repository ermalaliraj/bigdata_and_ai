package org.ea.oj.service;

import org.apache.jena.query.Query;
import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.QueryExecutionFactory;
import org.apache.jena.query.QueryFactory;
import org.ea.oj.dto.ActOJDto;
import org.ea.oj.repository.OJDocumentProvider;
import org.ea.oj.repository.OJDocumentProviderImpl;
import org.ea.oj.transformer.ConversionHelper;
import org.ea.util.SpringUtil;
import org.junit.Before;
import org.junit.Test;
import org.springframework.web.client.RestTemplate;

import javax.xml.transform.Transformer;
import java.util.List;

import static org.junit.Assert.assertNotNull;

public class ImportServiceImplTest extends AbstractSpringTest {

    private Transformer transformer;
    private ConversionHelper conversionHelper;
    private RestTemplate restTemplate;
    private OJDocumentProvider ojDocumentProvider;
    private ImportService importServiceImpl;

    @Before
    public void setup() {
        super.setup();
        transformer = SpringUtil.getBeanFromSpring("xsltTransformer");
        conversionHelper = new ConversionHelper(transformer);
        restTemplate = new RestTemplate();
        ojDocumentProvider = new OJDocumentProviderImpl(restTemplate);
        importServiceImpl = new ImportServiceImpl(ojDocumentProvider, conversionHelper);
    }

    @Test
    public void test_getAct_formexFormat() {
        String type = "reg";
        int year = 2016;
        int number = 679; //GDPR
        String document = importServiceImpl.getFormexActForYearAndNumber(type, year, number);
        assertNotNull(document);
    }

    @Test
    public void test_getAct_akomaNtosoFormat() {
        String type = "reg";
        int year = 2016;
        int number = 679;
        String document = importServiceImpl.getAknActForYearAndNumber(type, year, number);
        assertNotNull(document);
    }

    @Test
    public void test_getAllActsForYear_formexFormat() {
        String type = "reg";
        int year = 2021;
        List<ActOJDto> document = importServiceImpl.getFormexActsForYear(type, year);
        assertNotNull(document);
    }

    @Test
    public void test_getAllActsForYear_akomaNtosoFormat() {
        String type = "reg";
        int year = 2019;
        importServiceImpl.getAknActsForYear(type, year);
    }

    @Test
    public void compileSparql() {
        String sparqlQueryString=
                "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> \n"+
                        "select substr(str(?sub),0,1) ?sub ?super (count(?mid) as ?length) where {\n"+
                        "values ?sub { <http://dbpedia.org/ontology/Writer> }\n" +
                        "?sub rdfs:subClassOf* ?mid .\n"+
                        "?mid rdfs:subClassOf+ ?super .}\n"+
                        "group by ?sub ?super\n"+
                        "order by (?length)\n";
        Query query = QueryFactory.create(sparqlQueryString);
        QueryExecution qexec = QueryExecutionFactory.sparqlService("http://dbpedia.org/sparql",query);
    }
}
