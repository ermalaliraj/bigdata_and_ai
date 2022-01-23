package org.ea.oj.service;

import java.util.List;

public interface ImportService {

    String getFormexActForYearAndNumber(String type, int year, int number);

    List<String> getFormexActsForYear(String type, int year);

    String getAknActForYearAndNumber(String type, int year, int number);

    List<String> getAknActsForYears(String type, int year);

}
