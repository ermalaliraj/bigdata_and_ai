package org.ea.oj.repository;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.jena.query.Query;
import org.apache.jena.query.QueryExecutionFactory;
import org.apache.jena.query.ResultSet;
import org.apache.jena.query.ResultSetFormatter;
import org.apache.jena.sparql.engine.http.QueryEngineHTTP;
import org.ea.oj.dto.ActOJDto;
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
            Query query = SPARQLQueryCatalog.getActForYearAndNumber(type, year, number);
            String jsonOJResponse = callOJ(query);
            String urlAct = getUrlAct(jsonOJResponse);
            String doc = null;
            if (urlAct != null) {
                urlAct = urlAct + DOC_TYPE;
                LOG.trace("CELLAR/OJ Act url: " + urlAct);
                doc = restTemplate.getForObject(urlAct, String.class);
            }
            LOG.trace("Formex ACT from OJ: " + doc);
            return doc;
        } catch (IOException e) {
            throw new RuntimeException(String.format("Cannot get document from OJ for type {}, year {}, number {}", type, year, number), e);
        }
    }

    @Override
    public List<ActOJDto> getAllActsForYear(String type, int year) {
        Query query = SPARQLQueryCatalog.getAllActsForYear(type, year);
        String jsonOJResponse = callOJ(query);
        List<ActOJDto> urlActs = buildActDto(jsonOJResponse);
        LOG.info("Found {} documents in OJ. Start fetching one by one..", urlActs.size());
        for (int i = 0; i < urlActs.size(); i++) {
            ActOJDto actOJDto = urlActs.get(i);
            String url = actOJDto.getUrlActFormex();
            try {
                LOG.trace(i + " - CELLAR/OJ Act url: " + url);
                if (url != null && url.length() > 0) {
                    String doc = restTemplate.getForObject(url, String.class);
                    LOG.trace("Formex ACT from OJ: " + doc);
                    actOJDto.setActFormex(doc);
                }
            } catch (Exception e) {
//                throw new RuntimeException(String.format("Cannot get document from OJ for type {}, year {}, number {}, {}", type, years, i), e);
                LOG.error("Cannot get document from OJ for type {}, year {}, i {}, error: {}", type, year, i, e.getMessage());
            }
        }
        return urlActs;
    }

    private String callOJ(Query query) {
        QueryEngineHTTP qexec = null;
        try {
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

    private List<ActOJDto> buildActDto(String json) {
        List<ActOJDto> urlActs = new ArrayList<>();
        ObjectMapper mapper = new ObjectMapper();
        JsonNode rootNode = null;
        try {
            rootNode = mapper.readTree(json);
        } catch (IOException e) {
            LOG.trace("Cannot parse JSON file " + json);
        }

        JsonNode bindings = rootNode.get("results").get("bindings");
        for (int i = 0; i < bindings.size(); i++) {
            JsonNode row = bindings.get(i);
            ActOJDto actOJDto = new ActOJDto();
            actOJDto.setOjNr(getValue(row.get("callret-0")));
            actOJDto.setOjSeq(getValue(row.get("callret-1")));
            actOJDto.setDateDocument(getValue(row.get("date_document")));
            actOJDto.setOjLink(getValue(row.get("OJ")));
            actOJDto.setUrlActFormex(getValue(row.get("fmx4_act")));
            urlActs.add(actOJDto);
        }
        return urlActs;
    }

    private String getValue(JsonNode jsonNode) {
        String val = "";
        if (jsonNode != null && jsonNode.get("value") != null) {
            val = jsonNode.get("value").textValue();
        }
        return val;
    }

}
