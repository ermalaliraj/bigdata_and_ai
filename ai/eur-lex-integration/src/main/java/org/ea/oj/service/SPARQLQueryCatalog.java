package org.ea.oj.service;

import org.apache.jena.query.ParameterizedSparqlString;
import org.apache.jena.query.Query;

import java.util.List;

public class SPARQLQueryCatalog {

    public static Query getActForYearAndNumber(String type, int year, int number) {
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
        return queryStr.asQuery();
    }

    public static Query getAllActsForYears(String type, List<Integer> years) {
        String yearsIn = "";
        for (int year : years) {
            yearsIn += "'" + year + "',";
        }
        if (yearsIn.length() > 0) {
            yearsIn = yearsIn.substring(0, yearsIn.length() - 1);
        }

        ParameterizedSparqlString queryStr = new ParameterizedSparqlString();
        queryStr.setNsPrefix("cdm", "http://publications.europa.eu/ontology/cdm#");
        queryStr.setNsPrefix("owl", "http://www.w3.org/2002/07/owl#");
        queryStr.append(
                "PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>\n" +
                        "SELECT distinct ?fmx4_act \n" +
                        "WHERE \n" +
                        "{\n" +
                        "\t?work cdm:resource_legal_eli ?eli.\n" +
                        "\t?work cdm:work_date_document ?date_document.\n" +
                        "\t\tFILTER(substr(str(?date_document),1,4) IN (" + yearsIn + "))\n" +
                        "\t?work owl:sameAs ?OJ.\n" +
                        "\t\tFILTER(regex(str(?OJ),'/oj/'))\n" +
                        "\t\tOPTIONAL{?exp cdm:expression_title ?title.\n" +
                        "\t\t\t?exp cdm:expression_uses_language ?lang.\n" +
                        "\t\t\t?exp cdm:expression_belongs_to_work ?work.\n" +
                        "\t\t\tFILTER(?lang =<http://publications.europa.eu/resource/authority/language/ENG>)\n" +
                        "\t\t\tOPTIONAL{?manif_fmx4 cdm:manifestation_manifests_expression ?exp.\n" +
                        "\t\t\t\t?manif_fmx4 cdm:manifestation_type ?type_fmx4.\n" +
                        "\t\t\t\tFILTER(str(?type_fmx4)='fmx4')\n" +
                        "\t\t\t}\n" +
                        "\t}\n" +
                        "\tBIND(IF(BOUND(?manif_fmx4),IRI(concat(?manif_fmx4,\"/DOC_2\")),\"\") as ?fmx4_act)\n" +
                        "} limit 100");
        return queryStr.asQuery();
    }
}
