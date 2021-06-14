package org.ea.oj.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.jena.query.ParameterizedSparqlString;
import org.apache.jena.query.Query;
import org.apache.jena.query.QueryExecutionFactory;
import org.apache.jena.query.ResultSet;
import org.apache.jena.query.ResultSetFormatter;
import org.apache.jena.sparql.engine.http.QueryEngineHTTP;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestOperations;

import java.io.ByteArrayOutputStream;
import java.io.IOException;

@Component
public class OJDocumentProviderImpl implements OJDocumentProvider {
    private static Logger LOG = LoggerFactory.getLogger(OJDocumentProviderImpl.class);

    private static String ojUrl = "http://publications.europa.eu/webapi/rdf/sparql";
    private static final String DOC_TYPE = "/DOC_2";
    private static final String PARAM_DEBUG_VALUE = "on";
    private static final long PARAM_TIMEOUT_VALUE = 60000;
    private static final String PARAM_FORMAT_VALUE = "application/sparql-results+json";

    private final RestOperations restTemplate;

    @Autowired
    public OJDocumentProviderImpl(RestOperations restTemplate) {
        this.restTemplate = restTemplate;
    }

    @Override
    public String getFormexDocument(String type, int year, int number) {
        try {
            String urlDocument = getOJFormexDocumentUrl(type, year, number);
            LOG.trace("OJFormexDocumentUrl: " + urlDocument);
            String formexDocument = null;
            if (urlDocument != null) {
                urlDocument = urlDocument + DOC_TYPE;
                formexDocument = restTemplate.getForObject(urlDocument, String.class);
            }
            LOG.trace("FormexDocument: \n" + formexDocument);
            return formexDocument;
        } catch (IOException e) {
            throw new RuntimeException(String.format("Cannot get document from OJ for type {}, year {}, number {}", type, year, number), e);
        }
    }

    private String getOJFormexDocumentUrl(String type, int year, int number) throws IOException {
        QueryEngineHTTP qexec = null;
        try {
            ParameterizedSparqlString queryStr = new ParameterizedSparqlString();
            queryStr.setNsPrefix("cdm", "http://publications.europa.eu/ontology/cdm#");
            queryStr.append("SELECT DISTINCT ?manifestation ");
            queryStr.append("where {");
            queryStr.append(" ?work cdm:resource_legal_eli ?eli . filter(?eli = 'http://data.europa.eu/eli/");
            queryStr.append(type);
            queryStr.append("/");
            queryStr.append(year);
            queryStr.append("/");
            queryStr.append(number);
            queryStr.append("/oj'");
            queryStr.append("^^");
            queryStr.appendIri("http://www.w3.org/2001/XMLSchema#anyURI");
            queryStr.append(") ");
            queryStr.append(" ?work ^cdm:expression_belongs_to_work ?expression . ");
            queryStr.append("?expression cdm:expression_uses_language ?lng. ");
            queryStr.append("filter(?lng=");
            queryStr.appendIri("http://publications.europa.eu/resource/authority/language/ENG");
            queryStr.append(") ");
            queryStr.append("?manifestation cdm:manifestation_manifests_expression ?expression ; ");
            queryStr.append("cdm:manifestation_type ?type filter(regex(str(?type),'fmx4'))");
            queryStr.append("}");
            Query query = queryStr.asQuery();

            qexec = QueryExecutionFactory.createServiceRequest(ojUrl, query);
            qexec.addDefaultGraph("");
            qexec.addParam("debug", PARAM_DEBUG_VALUE);
            qexec.addParam("timeout", String.valueOf(PARAM_TIMEOUT_VALUE));
            qexec.addParam("format", PARAM_FORMAT_VALUE);
            qexec.setTimeout(PARAM_TIMEOUT_VALUE, PARAM_TIMEOUT_VALUE);

            LOG.trace("OJ Sparql URL: " + ojUrl);
            LOG.trace("OJ Sparql Query: \n{}", qexec.getQuery().toString(qexec.getQuery().getSyntax()));
            ResultSet results = qexec.execSelect();
            ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
            ResultSetFormatter.outputAsJSON(outputStream, results);
            String json = new String(outputStream.toByteArray());
            LOG.trace("OJ Sparql Response: \n{}", json);

            return getDocumentUrl(json);
        } finally {
            if (qexec != null) {
                qexec.close();
            }
        }
    }

    private String getDocumentUrl(String json) throws IOException {
        String uriDocument = null;
        ObjectMapper mapper = new ObjectMapper();
        JsonNode rootNode = mapper.readTree(json);
        JsonNode bindings = rootNode.get("results").get("bindings");
        if (bindings.size() > 0 && bindings.get(0) != null) {
            JsonNode manifestation = bindings.get(0).get("manifestation");
            uriDocument = manifestation.size() > 0 ? manifestation.get("value").textValue() : null;
        }
        return uriDocument;
    }

}
