package org.ea.oj.service;

import org.apache.commons.io.FileUtils;
import org.ea.oj.dto.ActOJDto;
import org.ea.oj.repository.OJDocumentProvider;
import org.ea.oj.transformer.ConversionHelper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.File;
import java.nio.charset.StandardCharsets;
import java.util.List;

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
    public String getFormexActForYearAndNumber(String type, int year, int number) {
        return ojDocumentProvider.getActForYearAndNumber(type, year, number);
    }

    @Override
    public List<ActOJDto> getFormexActsForYear(String type, int year) {
        return ojDocumentProvider.getAllActsForYear(type, year);
    }

    @Override
    public String getAknActForYearAndNumber(String type, int year, int number) {
        String aknDocument = null;
        String formexDocument = getFormexActForYearAndNumber(type, year, number);
        if (formexDocument != null) {
            LOG.info("Found in  OJ {}/{}/{} document of {} length", type, year, number, formexDocument.length());
            try {
                String fileName = OJ_OUTPUT_PATH + type + "_" + year + "_" + number;
                aknDocument = conversionHelper.convertFormexToAKN(formexDocument);
                FileUtils.writeByteArrayToFile(new File(fileName + "_akn.xml"), aknDocument.getBytes(StandardCharsets.UTF_8));
            } catch (Exception e) {
                throw new RuntimeException(String.format("Cannot create AKN document type/year/nr {}/{}/{}", type, year, number), e);
            }
        } else {
            LOG.info("Didn't found in OJ  {}/{}/{}", type, year, number);
        }
        return aknDocument;
    }

    @Override
    public List<ActOJDto> getAknActsForYear(String type, int year) {
        String aknDocument;
        List<ActOJDto> formexActsForYear = getFormexActsForYear(type, year);

        int i;
        for (i = 0; i < formexActsForYear.size(); i++) {
            try {
                ActOJDto actOJDto = formexActsForYear.get(i);
                String fileName = OJ_OUTPUT_PATH + type + "_" + year + "_nr-" + actOJDto.getOjNr() + "_seq-" + actOJDto.getOjSeq();
                aknDocument = conversionHelper.convertFormexToAKN(actOJDto.getActFormex());
                FileUtils.writeByteArrayToFile(new File(fileName + "_akn.xml"), aknDocument.getBytes(StandardCharsets.UTF_8));
            } catch (Exception e) {
//                throw new RuntimeException(String.format("Cannot create AKN file for Act {}", formexActsForYear.get(i).toString()), e);
                LOG.error("Cannot create AKN file {} iteration, for Act {} , error: {}", i, formexActsForYear.get(i).toString(), e.getMessage());
            }
        }
        LOG.error("Processed {} documents", i);
        return formexActsForYear;
    }

}
