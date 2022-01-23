package org.ea.oj.repository;

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
                        "}");
        return queryStr.asQuery();
    }

    public static Query getAllActsForYear(String type, int year) {
        ParameterizedSparqlString queryStr = new ParameterizedSparqlString();
        queryStr.setNsPrefix("cdm", "http://publications.europa.eu/ontology/cdm#");
        queryStr.setNsPrefix("owl", "http://www.w3.org/2002/07/owl#");
        queryStr.append(
                "SELECT DISTINCT substr(str(?OJ),52,3) substr(str(?OJ),58,4) ?OJ ?date_document ?fmx4_act \n" +
                        "WHERE\n" +
                        "  { ?work cdm:resource_legal_eli ?eli ; cdm:work_date_document ?date_document\n" +
                        "\t\tFILTER(regex(str(?eli),'/" + type + "/'))\n" +
                        "\t\tFILTER(substr(str(?date_document), 1, 4) IN (\"" + year + "\"))\n" +
                        "    ?work owl:sameAs  ?OJ\n" +
                        "    FILTER regex(str(?OJ), \"/oj/\")\n" +
                        "    OPTIONAL\n" +
                        "      { ?exp  cdm:expression_title ?title ;\n" +
                        "              cdm:expression_uses_language ?lang ;\n" +
                        "              cdm:expression_belongs_to_work ?work\n" +
                        "        FILTER(?lang = <http://publications.europa.eu/resource/authority/language/ENG>)\n" +
                        "        OPTIONAL\n" +
                        "          { ?manif_fmx4 cdm:manifestation_manifests_expression  ?exp ;\n" +
                        "\t\t\t\t\t\tcdm:manifestation_type  ?type_fmx4\n" +
                        "            FILTER(str(?type_fmx4) = \"fmx4\")\n" +
                        "\t\t\tBIND(STRLEN(?exp) AS ?len_o)  \n" +
                        "          }\n" +
                        "      }\n" +
                        "\t  FILTER(?len_o != 0) \n" +
                        "    BIND(if(bound(?manif_fmx4), iri(concat(?manif_fmx4, \"/DOC_2\")), \"\") AS ?fmx4_act)\n" +
                        "  }\n");
        return queryStr.asQuery();
    }
}
