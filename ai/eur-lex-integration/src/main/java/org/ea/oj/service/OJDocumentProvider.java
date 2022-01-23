package org.ea.oj.service;

import java.util.List;

public interface OJDocumentProvider {

    String getActForYearAndNumber(String type, int year, int number);

    List<String> getAllActsForYears(String type, List<Integer> year);

}
