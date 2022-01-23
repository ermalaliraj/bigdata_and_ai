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
package org.ea.oj.transformer;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;

import javax.xml.transform.OutputKeys;
import javax.xml.transform.Source;
import javax.xml.transform.Transformer;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.stream.StreamSource;
import java.io.StringReader;
import java.io.StringWriter;

@Component
public class ConversionHelper {
    private static final Logger LOG = LoggerFactory.getLogger(ConversionHelper.class);

    final private Transformer transformer;

    @Autowired
    public ConversionHelper(@Qualifier("xsltTransformer") Transformer transformer) {
        this.transformer = transformer;
    }

    public String convertFormexToAKN(String formexDocument) {
        if(formexDocument == null) {
            return null;
        }
        try {
            transformer.setOutputProperty(OutputKeys.ENCODING, "UTF-8");
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");

            Source xmlSource = new StreamSource(new StringReader(formexDocument));
            StringWriter outWriter = new StringWriter();
            StreamResult result = new StreamResult(outWriter);
            transformer.transform(xmlSource, result);
            StringBuffer sb = outWriter.getBuffer();
//            LOG.trace("Document in Akoma Ntoso format: \n" + sb.toString());
            return sb.toString();
        } catch (Exception e) {
            throw new RuntimeException("Unable to convert to AKN", e);
        }
    }
}
