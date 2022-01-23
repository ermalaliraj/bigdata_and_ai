package org.ea.oj.repository;

import org.ea.oj.dto.ActOJDto;

import java.util.List;

public interface OJDocumentProvider {

    String getActForYearAndNumber(String type, int year, int number);

    List<ActOJDto> getAllActsForYear(String type, int year);

}
