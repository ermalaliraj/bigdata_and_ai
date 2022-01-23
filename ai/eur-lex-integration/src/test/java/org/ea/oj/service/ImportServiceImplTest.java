/*
 * Copyright 2017 European Commission
 *
 * Licensed under the EUPL, Version 1.2 or – as soon they will be approved by the European Commission - subsequent versions of the EUPL (the "Licence");
 * You may not use this work except in compliance with the Licence.
 * You may obtain a copy of the Licence at:
 *
 *     https://joinup.ec.europa.eu/software/page/eupl
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the Licence for the specific language governing permissions and limitations under the Licence.
 */
package org.ea.oj.service;

import org.ea.util.SpringUtil;
import org.junit.Before;
import org.junit.Test;
import org.springframework.web.client.RestTemplate;

import javax.xml.transform.Transformer;
import java.util.List;

import static org.junit.Assert.assertNotNull;

public class ImportServiceImplTest extends AbstractSpringTest {

    private Transformer transformer;
    private ConversionHelper conversionHelper;
    private RestTemplate restTemplate;
    private OJDocumentProvider ojDocumentProvider;
    private ImportService importServiceImpl;

    @Before
    public void setup() {
        super.setup();
        transformer = SpringUtil.getBeanFromSpring("xsltTransformer");
        conversionHelper = new ConversionHelper(transformer);
        restTemplate = new RestTemplate();
        ojDocumentProvider = new OJDocumentProviderImpl(restTemplate);
        importServiceImpl = new ImportServiceImpl(ojDocumentProvider, conversionHelper);
    }

    @Test
    public void test_getAct_formexFormat() {
        String type = "reg";
        int year = 2016;
        int number = 679; //GDPR
        String document = importServiceImpl.getFormexActForYearAndNumber(type, year, number);
        assertNotNull(document);
    }

    @Test
    public void test_getAct_akomaNtosoFormat() {
        String type = "reg";
        int year = 2016;
        int number = 679;
        String document = importServiceImpl.getAknActForYearAndNumber(type, year, number);
        assertNotNull(document);
    }

    @Test
    public void test_getAllActsForYear_formexFormat() {
        String type = "reg";
        int year = 2021;
        List<String> document = importServiceImpl.getFormexActsForYear(type, year);
        assertNotNull(document);
    }

    @Test
    public void test_getAllActForYear_akomaNtosoFormat() {
        String type = "reg";
        int year = 2020;
        importServiceImpl.getAknActsForYears(type, year);
    }

}
