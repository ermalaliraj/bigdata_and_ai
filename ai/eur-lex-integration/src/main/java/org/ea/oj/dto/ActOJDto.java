package org.ea.oj.dto;

import org.apache.commons.lang3.builder.ReflectionToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;

public class ActOJDto {

    private String ojNr;
    private String ojSeq;
    private String ojLink;
    private String urlActFormex;
    private String actFormex;
    private String dateDocument;

    public String getOjNr() {
        return ojNr;
    }

    public void setOjNr(String ojNr) {
        this.ojNr = ojNr;
    }

    public String getOjSeq() {
        return ojSeq;
    }

    public void setOjSeq(String ojSeq) {
        this.ojSeq = ojSeq;
    }

    public String getOjLink() {
        return ojLink;
    }

    public void setOjLink(String ojLink) {
        this.ojLink = ojLink;
    }

    public String getUrlActFormex() {
        return urlActFormex;
    }

    public void setUrlActFormex(String urlActFormex) {
        this.urlActFormex = urlActFormex;
    }

    public String getDateDocument() {
        return dateDocument;
    }

    public void setDateDocument(String dateDocument) {
        this.dateDocument = dateDocument;
    }

    public String getActFormex() {
        return actFormex;
    }

    public void setActFormex(String actFormex) {
        this.actFormex = actFormex;
    }

    public String toString() {
        ReflectionToStringBuilder rtsb = new ReflectionToStringBuilder(this, ToStringStyle.SHORT_PREFIX_STYLE);
        rtsb.setExcludeNullValues(true);
        return rtsb.toString();
    }
}
