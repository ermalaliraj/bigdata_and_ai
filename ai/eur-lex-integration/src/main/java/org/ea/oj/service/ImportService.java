package org.ea.oj.service;

import java.util.List;

public interface ImportService {

    String getFormexActForYearAndNumber(String type, int year, int number);

    List<String> getFormexActsForYears(String type, List<Integer> years);

    String getAknActForYearAndNumber(String type, int year, int number);

    List<String> getAknActsForYears(String type, List<Integer> years);

}
