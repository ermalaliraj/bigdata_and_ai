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

import org.apache.commons.io.FileUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.File;
import java.nio.charset.StandardCharsets;

@Service
class ImportServiceImpl implements ImportService {

    private static final Logger LOG = LoggerFactory.getLogger(ImportServiceImpl.class);

    static String OJ_OUTPUT_PATH = "output/oj/";

    private OJDocumentProvider ojDocumentProvider;
    private ConversionHelper conversionHelper;

    @Autowired
    ImportServiceImpl(OJDocumentProvider ojDocumentProvider, ConversionHelper conversionHelper) {
        this.ojDocumentProvider = ojDocumentProvider;
        this.conversionHelper = conversionHelper;
    }

    @Override
    public String getFormexDocument(String type, int year, int number) {
        return ojDocumentProvider.getFormexDocument(type, year, number);
    }

    @Override
    public String getAknDocument(String type, int year, int number) {
        String aknDocument = null;
        String formexDocument = getFormexDocument(type, year, number);
        if (formexDocument != null) {
            LOG.info("Found in  OJ for {}/{}/{} document of {} length" ,  type,  year , number, formexDocument.length());
            try {
                String fileName = OJ_OUTPUT_PATH + type + "_" + year + "_" + number;
//                FileUtils.writeByteArrayToFile(new File(fileName + "_oj.xml"), formexDocument.getBytes(StandardCharsets.UTF_8));
                aknDocument = conversionHelper.convertFormexToAKN(formexDocument);
                FileUtils.writeByteArrayToFile(new File(fileName + "_akn.xml"), aknDocument.getBytes(StandardCharsets.UTF_8));
            } catch (Exception e) {
                throw new RuntimeException(String.format("Cannot get AKN from OJ for type/year/nr {}/{}/{}", type, year, number), e);
            }
        } else {
            LOG.info("Didn't found in OJ for " + type + "/" + year + "/" + number);
        }
        return aknDocument;
    }

}
