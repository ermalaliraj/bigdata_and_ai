package org.ea.oj.service;

import org.ea.oj.dto.ActOJDto;

import java.util.List;

public interface ImportService {

    String getFormexActForYearAndNumber(String type, int year, int number);

    List<ActOJDto> getFormexActsForYear(String type, int year);

    String getAknActForYearAndNumber(String type, int year, int number);

    List<ActOJDto> getAknActsForYear(String type, int year);

}
