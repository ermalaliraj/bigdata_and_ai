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
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.web.client.RestTemplate;

import javax.xml.transform.Transformer;

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
    public void test_getFormexDocument() {
        String type = "reg";
        int year = 2013;
        int number = 1303;
        String document = importServiceImpl.getFormexDocument(type, year, number);
        assertNotNull(document);
    }

    @Test
    public void test_getAknDocument() throws InterruptedException {
        String type = "reg";
        int year = 2013;
        int number = 123;
        for(int i = 6; i<= 100; i++){
            String document = importServiceImpl.getAknDocument(type, year, i);
            Thread.sleep(1000);
        }
    }
}
