package org.ea.oj.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
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
import java.util.ArrayList;
import java.util.List;

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
    public String getActForYearAndNumber(String type, int year, int number) {
        try {
            String jsonOJResponse = getActForYearAndNumberFromOJ(type, year, number);
            String urlAct = getUrlAct(jsonOJResponse);
            String doc = null;
            if (urlAct != null) {
                urlAct = urlAct + DOC_TYPE;
                LOG.trace("CELLAR url: " + urlAct);
                doc = restTemplate.getForObject(urlAct, String.class);
            }
            LOG.trace("Formex ACT from OJ: " + doc);
            return doc;
        } catch (IOException e) {
            throw new RuntimeException(String.format("Cannot get document from OJ for type {}, year {}, number {}", type, year, number), e);
        }
    }

    @Override
    public List<String> getAllActsForYears(String type, List<Integer> years) {
        String jsonOJResponse = getUrlActsFromOJ(type, years);
        List<String> urlActs = getUrlActs(jsonOJResponse);
        List<String> acts = new ArrayList<>();
        for (int i = 0; i < urlActs.size(); i++) {
            String url = urlActs.get(i);
            try {
                LOG.trace(i + " - CELLAR url: " + url);
                if (url != null && url.length() > 0) {
                    String doc = restTemplate.getForObject(url, String.class);
                    LOG.trace("Formex ACT from OJ: " + doc);
                    acts.add(doc);
                }
            } catch (Exception e) {
//                throw new RuntimeException(String.format("Cannot get document from OJ for type {}, year {}, number {}, {}", type, years, i), e);
                LOG.error("Cannot get document from OJ for type {}, year {}, i {}, error: {}", type, years, i, e.getMessage());
            }
        }
        return acts;

    }

    private String getUrlActsFromOJ(String type, List<Integer> years) {
        QueryEngineHTTP qexec = null;
        try {
            Query query = SPARQLQueryCatalog.getAllActsForYears(type, years);

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
            LOG.trace("OJ Sparql Response as json: \n{}", json);
            return json;
        } finally {
            if (qexec != null) {
                qexec.close();
            }
        }
    }

    private String getActForYearAndNumberFromOJ(String type, int year, int number) {
        QueryEngineHTTP qexec = null;
        try {
            Query query = SPARQLQueryCatalog.getActForYearAndNumber(type, year, number);

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
            LOG.trace("OJ Sparql Response as json: \n{}", json);
            return json;
        } finally {
            if (qexec != null) {
                qexec.close();
            }
        }
    }

    private String getUrlAct(String json) throws IOException {
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

    private List<String> getUrlActs(String json) {
        List<String> urlActs = new ArrayList<>();
        ObjectMapper mapper = new ObjectMapper();
        JsonNode rootNode = null;
        try {
            rootNode = mapper.readTree(json);
        } catch (IOException e) {
            LOG.trace("Cannot parse JSON file " + json);
        }

        JsonNode bindings = rootNode.get("results").get("bindings");
        for (int i = 0; i < bindings.size(); i++) {
            JsonNode fmx4_act = bindings.get(i).get("fmx4_act");
            if (fmx4_act != null && fmx4_act.size() > 0 && fmx4_act.get("value") != null) {
                urlActs.add(fmx4_act.get("value").textValue());
            }
        }
        return urlActs;
    }

}
