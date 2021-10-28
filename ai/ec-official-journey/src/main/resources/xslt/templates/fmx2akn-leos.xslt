<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:fn="http://www.w3.org/2005/xpath-functions" xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" xpath-default-namespace="" xmlns:fmx="http://formex.publications.europa.eu/schema/formex-05.21-20110601.xd" xmlns:leos="urn:eu:europa:ec:leos">
    <!-- author : V. Parisse
        Changes :
- 2017-05-18 : a list is not inside a subparagraph
- complex alinea, table, formula, list of definition
- 30-06-2017 
- complete some metadata (FRBRlanguage, FRBRcountry, FRBRformat
- modify the namespace: http://docs.oasis-open.org/legaldocml/ns/akn/3.0
- restructure the NP/TXT treatment
- 11-07-2017
- longTitle : 1 <p>; docPurpose; docType for all the second line; empty docStage
- every identifier -> GUID
- add the number of the footnote
- intro recitals in a <block>
- identify title, part, chapter, section, subsection ; hcontainer for other
- 2017-09-06 : accept "sub-section" and "subsection" for a subsection
- when ARTICLE has no ART_STI, generates an empty heading.
-2017-10-10 : only one <p> in a recital
2017-10-24 : correct the authorialNote in recital
2017-10-26 : attribute leos:notSupported added for articles containing modification on other act or mathematical formulas.
2018-02-08 : point temporary changed, after need to be indent
2018-03-02 : generated GUID starts with a "_" if identifier starts with a digit
2018-03-27 : replace &nbsp; by ' '
2018-03-27 : GUID for article are random numbers (no more coming from the id of Formex)
2018-03-27 : remove GUID for authorialNote and paragraph
2018-04-12 : remove spaces and indentation (xml:output  indent="no" )
2019-01-11 : correct recitalsIntro in recitals, formulas and signatory
2019-06-07 : escape " and ' characters. Cleanup extra whitespace in texts elements.
2019-07-02 : article/alinea - fixed LIST alone inside a PARAGRAPH. Now LIST is created inside a PARAGRAPH together with previous P
                as SUBPARAGRAPH or an empty SUBPARAGRAPH is there's no previous P (PAR -> SUBPAR + LIST)
2019-09-27 : escape ‘, ’, “, ”, – and — characters.
2019-10-03 : manage the indent
-->
    <xsl:character-map name="special-characters">
        <xsl:output-character character="&#160;" string=" "/>
        <xsl:output-character character="&#34;" string="&amp;quot;"/>
        <xsl:output-character character="&#8220;" string="&amp;quot;"/>
        <xsl:output-character character="&#8221;" string="&amp;quot;"/>
        <xsl:output-character character="&#39;" string="&amp;apos;"/>
        <xsl:output-character character="&#8216;" string="&amp;apos;"/>
        <xsl:output-character character="&#8217;" string="&amp;apos;"/>
        <xsl:output-character character="&#8211;" string="&amp;#45;"/>
        <xsl:output-character character="&#8212;" string="&amp;#45;"/>
    </xsl:character-map>
    <xsl:output method="xml" version="1.0" encoding="UTF-8" indent="no" exclude-result-prefixes="fn" use-character-maps="special-characters"/>
    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>
    <!-- -->
    <xsl:template match="text()">
        <xsl:value-of select="replace(replace(., '&#160;', ' '), '( +){2,}', ' ')"/>
    </xsl:template>
    <!-- -->
    <xsl:template match="ACT">
        <xsl:element name="akomaNtoso">
        <xsl:namespace name="fmx" select="'http://formex.publications.europa.eu/schema/formex-05.21-20110601.xd'"/>
         <xsl:namespace name="leos" select="'urn:eu:europa:ec:leos'"/>
         <xsl:namespace name="xs" select="'http://www.w3.org/2001/XMLSchema'"/>
           <xsl:element name="bill">
                <xsl:attribute name="name"/>
                <meta>
                    <identification source="~COM">
                        <FRBRWork>
                            <FRBRthis value=""/>
                            <FRBRuri value=""/>
                            <FRBRdate date="2999-01-01" name=""/>
                            <FRBRauthor href=""/>
                            <FRBRcountry value=""/>
                        </FRBRWork>
                        <FRBRExpression>
                            <FRBRthis value=""/>
                            <FRBRuri value=""/>
                            <FRBRdate date="2999-01-01" name=""/>
                            <FRBRauthor href=""/>
                            <FRBRlanguage language="eng"/>
                        </FRBRExpression>
                        <FRBRManifestation>
                            <FRBRthis value=""/>
                            <FRBRuri value=""/>
                            <FRBRdate date="2999-01-01" name=""/>
                            <FRBRauthor href=""/>
                        </FRBRManifestation>
                    </identification>
                </meta>
                <xsl:apply-templates select="TITLE"/>
                <xsl:apply-templates select="PREAMBLE"/>
                <xsl:apply-templates select="ENACTING.TERMS"/>
                <xsl:apply-templates select="FINAL/SIGNATURE"/>
            </xsl:element>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <!--                                                   The act title -->
    <xsl:template match="ACT/TITLE">
        <xsl:element name="preface">
            <xsl:element name="longTitle">
                <xsl:element name="p">
                    <xsl:element name="docStage"></xsl:element>
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:element>
            <xsl:if test="TI/P[position()=4]">
                <xsl:apply-templates select="TI/P[position()=4]" mode="EEArelevance"/>
            </xsl:if>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="ACT/TITLE/TI/P" mode="EEArelevance">
        <xsl:element name="container">
            <xsl:attribute name="name">EEArelevance</xsl:attribute>
            <xsl:element name="p">
                <xsl:apply-templates/>
            </xsl:element>
        </xsl:element>
    </xsl:template>
    <xsl:template match="ACT/TITLE/TI/P">
        <xsl:choose>
            <xsl:when test="position()=1">
                <xsl:element name="docType">
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="position()=3">
                <xsl:element name="docPurpose">
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="position() > 3"></xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!-- -->

    <xsl:template match="PREAMBLE">
        <xsl:element name="preamble">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="PREAMBLE.INIT">
        <xsl:element name="formula">
            <xsl:attribute name="name">actingEntity</xsl:attribute>
            <xsl:element name="p">
                <xsl:apply-templates/>
            </xsl:element>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="GR.VISA">
        <xsl:element name="citations">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="VISA">
        <xsl:element name="citation">
            <xsl:element name="p">
                <xsl:apply-templates/>
            </xsl:element>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="GR.CONSID">
        <xsl:element name="recitals">
            <xsl:attribute name="xml:id" select="concat('recs_',generate-id())"/><!-- specific for Leos -->
            <xsl:element name="intro">
                <xsl:element name="p">
                    <xsl:apply-templates select="GR.CONSID.INIT"/>
                </xsl:element>
            </xsl:element>
            <xsl:apply-templates select="*[not(name()='GR.CONSID.INIT')]"/>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="CONSID">
        <xsl:element name="recital">
            <xsl:attribute name="xml:id" select="concat('rec_',generate-id())"/><!-- specific for Leos -->
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="PREAMBLE.FINAL">
        <xsl:element name="formula">
            <xsl:attribute name="name">enactingFormula</xsl:attribute>
            <xsl:element name="p">
                <xsl:apply-templates/>
            </xsl:element>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="NOTE">
        <xsl:element name="authorialNote">
            <xsl:attribute name="placement">bottom</xsl:attribute>
            <xsl:attribute name="marker" select="count(preceding::NOTE) + 1"/>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="ENACTING.TERMS">
        <xsl:element name="body">
            <xsl:apply-templates/>
            <xsl:if test="/ACT/FINAL/P">
                <xsl:apply-templates select="/ACT/FINAL/P"/>
            </xsl:if>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="DIVISION">
        <xsl:variable name="title"><xsl:copy-of  select="TITLE/TI" /></xsl:variable>
        <xsl:choose>
            <xsl:when test="starts-with(lower-case($title), 'part')">
                <xsl:element name="part">
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="starts-with(lower-case($title), 'title')">
                <xsl:element name="title">
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="starts-with(lower-case($title), 'chapter')">
                <xsl:element name="chapter">
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="starts-with(lower-case($title), 'section')">
                <xsl:element name="section">
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="starts-with(lower-case($title), 'sub-section') or starts-with(lower-case($title), 'subsection')">
                <xsl:element name="subsection">
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>    <!-- unknown structure -->
                <xsl:element name="hcontainer">
                    <xsl:attribute name="name">todefine</xsl:attribute>
					<xsl:text disable-output-escaping="yes">&lt;!-- &lt;leos:unknown></xsl:text>
					<xsl:element name="{local-name()}"><xsl:copy-of select="@*"/>
							<xsl:copy-of select="TITLE" exclude-result-prefixes="#all" />
					</xsl:element><xsl:text disable-output-escaping="yes">&lt;/leo:unknown> --></xsl:text>
                   <xsl:apply-templates/>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!-- -->
    <!-- -->
    <xsl:template match="ARTICLE">
        <xsl:element name="article">
            <xsl:attribute name="xml:id" select="concat('art_',generate-id())"/>
            <xsl:if test="descendant::QUOT.S or descendant::FORMULA.S or descendant::FORMULA or descendant::GR.SEQ[NP]">
				<xsl:attribute name="leos:compliant">false</xsl:attribute>
            </xsl:if>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="PARAG">
        <xsl:element name="paragraph">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="DIVISION/TITLE/TI/P | QUOT.S/TITLE/TI/P">
        <xsl:element name="num">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="DIVISION/TITLE/STI/P | QUOT.S/TITLE/STI/P">
        <xsl:element name="heading">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <!--  already treated -->
    <xsl:template match="DIVISION/TITLE/TI | QUOT.S/TITLE/TI | QUOT.S/TITLE | DIVISION/TITLE | DIVISION/TITLE/STI | QUOT.S/TITLE/STI | TI | GR.CONSID.INIT">
        <xsl:apply-templates/>
    </xsl:template>
    <!-- -->
    <xsl:template match="NO.PARAG">
        <xsl:element name="num">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="TI.ART">
        <xsl:element name="num">
            <xsl:apply-templates/>
        </xsl:element>
        <xsl:if test="not(following-sibling::STI.ART)">
            <xsl:element name="heading"></xsl:element>
        </xsl:if>
    </xsl:template>
    <!-- -->
    <xsl:template match="STI.ART | GR.TBL/TITLE/TI | GR.SEQ/TITLE/TI">
        <xsl:element name="heading">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="TBL/TITLE">
        <xsl:element name="caption">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="TBL/TITLE/TI">
        <xsl:apply-templates/>
    </xsl:template>
    <!-- -->
    <!-- -->
    <xsl:template match="TBL/TITLE/STI">
        <xsl:if test="preceding-sibling::TI">
            <xsl:element name="eol"/>
        </xsl:if>
        <xsl:apply-templates/>
    </xsl:template>
    <xsl:template match="ARTICLE/ALINEA | QUOT.S/ALINEA">
        <!-- ALINEA in ARTICLE is a <paragraph>
              ALINEA as mixed content = paragraph with content ; with subblock, see the treatment of this subblock. -->
        <xsl:choose>
            <xsl:when test="LIST | P | TBL| FORMULA.S | DLIST | GR.TBL | GR.SEQ">
                <xsl:apply-templates/>
                <!-- sometimes, ALINEA contains multiples block => each block is a unnumbered paragraph  -->
            </xsl:when>
            <xsl:otherwise>
                <!-- sometimes, the ALINEA contains text => it is a unnumbered paragraph with content (LEOS) -->
                <xsl:element name="paragraph">
                    <xsl:element name="content">
                        <xsl:element name="p">
                            <xsl:apply-templates/>
                        </xsl:element>
                    </xsl:element>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!-- -->
    <!-- -->
    <xsl:template match="PARAG/ALINEA">
        <!-- ALINEA in PARAG
          ALINEA as mixed content if not alone, = <subparagraph> with content ; with subblock, see the treatment of this subblock. -->
        <xsl:choose>
            <!-- !!! order of the cases are important !!!  -->
            <xsl:when test="LIST | P | TBL| FORMULA.S | DLIST | GR.TBL | GR.SEQ">
                <!-- if ALINEA contains block, each block is treated separately. -->
                <xsl:apply-templates/>
            </xsl:when>
            <xsl:when test="count(../ALINEA)  > 1">
                <!-- paragraph contains always alinea, even if only one block.  Subparagraph is only when multiple block. -->
                <xsl:element name="subparagraph">
                    <xsl:element name="content">
                        <xsl:element name="p">
                            <xsl:apply-templates/>
                        </xsl:element>
                    </xsl:element>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="content">
                    <xsl:element name="p">
                        <xsl:apply-templates/>
                    </xsl:element>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!-- -->
    	<xsl:template match="SUBDIV">
	<!-- he SUBDIV element is used to mark up a subdivision when the paragraphs or alineas in an article are grouped together; not covered by Leos -->
		<xsl:text disable-output-escaping="yes">&lt;!-- &lt;leos:unknown></xsl:text>
		<xsl:element name="{local-name()}"><xsl:copy-of select="@*"/>
		<xsl:copy-of select="TITLE" exclude-result-prefixes="#all" /></xsl:element><xsl:text disable-output-escaping="yes">&lt;/leo:unknown> --></xsl:text>
		<xsl:apply-templates select="*[not(name() = 'TITLE')]"/>
	</xsl:template>
	<!-- -->
    <!--                                                                NP -->
    <!-- -->
    <xsl:template match="NP[parent::GR.SEQ or parent::QUOT.S]">    <!-- amending act -->
        <xsl:element name="point">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <!--  -->
    <xsl:template match="NP[not(parent::ITEM or parent::GR.SEQ or parent::QUOT.S) and ancestor::ENACTING.TERMS]"> <!-- amending act -->
        <xsl:comment>not treated use of &lt;NP> </xsl:comment>
        <xsl:element name="p">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <!--  -->
    <!--  -->
	<xsl:template match="NP[parent::CONSID]">  <!-- one p for a recital -->
		<xsl:apply-templates select="NO.P"/>
		<xsl:element name="p">
			<xsl:apply-templates select="*[not(name()='NO.P')]"/>
		</xsl:element>
	</xsl:template>	
    <!-- -->
    <xsl:template match="NP">
        <xsl:apply-templates/>
    </xsl:template>
    <!-- -->
    <!--                        TXT  in NP in enacting terms -->
    <xsl:template match="NP/TXT[ancestor::ENACTING.TERMS]">
        <xsl:choose>
            <xsl:when test="LIST or FORMULA.S or TBL or DLIST or GR.TBL or GR.SEQ">
                <xsl:apply-templates/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:choose>
                    <xsl:when test="not(following-sibling::*)">
                        <xsl:choose>
                            <xsl:when test="(ancestor::TBL or ancestor::DLIST)">
                                <!-- upper element is an item in a blockList> -->
                                <xsl:element name="p">
                                    <xsl:apply-templates/>
                                </xsl:element>
                            </xsl:when>
                            <xsl:otherwise>
                                <!-- upper element is a point or an indent in a list. -->
                                <xsl:element name="content">
                                    <xsl:element name="p">
                                        <xsl:apply-templates/>
                                    </xsl:element>
                                </xsl:element>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:choose>
                            <xsl:when test="(ancestor::TBL or ancestor::DLIST)">
                                <!-- upper element is an item in a blockList> -->
                                <xsl:element name="p">
                                    <xsl:apply-templates/>
                                </xsl:element>
                            </xsl:when>
                            <xsl:otherwise>
                                <!-- block that don't contain sub-block in the case of multiple blocks -> = alinea -->
                                <xsl:element name="alinea">
                                    <xsl:element name="content">
                                        <xsl:element name="p">
                                            <xsl:apply-templates/>
                                        </xsl:element>
                                    </xsl:element>
                                </xsl:element>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
	<!-- -->
	<xsl:template match="TXT[ancestor::CONSID]"> <!-- one p for recital -->
			<xsl:apply-templates/>
	</xsl:template>	    
	<!-- -->
    <xsl:template match="TXT">
        <xsl:element name="p">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <!--  -->
    <xsl:template match="ITEM/P">
        <!-- item with no numbering -->
        <xsl:choose>
            <xsl:when test="LIST or FORMULA.S or TBL or DLIST or GR.TBL or GR.SEQ">
                <!-- P with subblock is not translated in AKN -->
                <xsl:apply-templates/>
            </xsl:when>
            <xsl:when test="(ancestor::TBL or ancestor::DLIST)">
                <!-- in <table>, only blockList is available -->
                <xsl:element name="p">
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="not(following-sibling::* | preceding-sibling::*)">
                <!-- one block in ITEM, this is the content. -->
                <xsl:element name="content">
                    <xsl:element name="p">
                        <xsl:apply-templates/>
                    </xsl:element>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="alinea">
                    <!-- block that don't contain sub-block in the case of multiple blocks -> = alinea -->
                    <!-- certainly to be reviewed -->
                    <xsl:element name="content">
                        <xsl:element name="p">
                            <xsl:apply-templates/>
                        </xsl:element>
                    </xsl:element>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!-- -->
    <xsl:template match="PREAMBLE.INIT/P | PREAMBLE.FINAL/P | STI.ART/P | GR.TBL/TITLE/TI/P | GR.SEQ/TITLE/TI/P | TBL/TITLE/TI/P | TBL/TITLE/STI/P">
        <!-- the P is optional, sometimes it is there, sometimes not.  The treatment is done in the parent element so the P is not treated. -->
        <xsl:apply-templates/>
    </xsl:template>
    <!-- -->
    
    <!--   -->
    <xsl:template match="GR.TBL | GR.SEQ[TBL]">
		<xsl:apply-templates/>
	</xsl:template>
   <!--   -->
    <xsl:template match="GR.SEQ">
        <!-- P in alinea :  in article is paragraph ;  in paragraph is subparagraph ; in the other case, is alinea  -->
        <xsl:choose>
            <xsl:when test="parent::*/parent::ARTICLE">
                <!-- hypothesis: ARTICLE is always composed of ALINEA or PARAG -->
                <xsl:element name="paragraph">
                    <xsl:attribute name="class"><xsl:value-of select="name()"/></xsl:attribute>
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="parent::*/parent::PARAG">
                <!-- hypothesis: PARAG is always composed of ALINEA -->
                <xsl:element name="subparagraph">
                    <xsl:attribute name="class"><xsl:value-of select="name()"/></xsl:attribute>
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="parent::NP">
                <xsl:element name="alinea">
                    <xsl:attribute name="class"><xsl:value-of select="name()"/></xsl:attribute>
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:comment>
                    <xsl:value-of select="name()"/> is a special position => not treated </xsl:comment>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>	
	<xsl:template match="GR.TBL/TITLE | GR.SEQ[TBL]/TITLE">
        <!-- P in alinea :  in article is paragraph ;  in paragraph is subparagraph ; in the other case, is alinea  -->
        <xsl:choose>
            <xsl:when test="parent::*/parent::*/parent::ARTICLE">
                <!-- hypothesis: ARTICLE is always composed of ALINEA or PARAG -->
                <xsl:element name="paragraph">
                    <xsl:attribute name="class"><xsl:value-of select="name()"/></xsl:attribute>
                    <xsl:element name="content">
						<xsl:element name="p">
						<xsl:apply-templates select="TI/P"/>
						</xsl:element>					
					</xsl:element>
                </xsl:element>
            </xsl:when>
            <xsl:when test="parent::*/parent::*/parent::PARAG">
                <!-- hypothesis: PARAG is always composed of ALINEA -->
                <xsl:element name="subparagraph">
                    <xsl:attribute name="class"><xsl:value-of select="name()"/></xsl:attribute>
                    <xsl:element name="content">
						<xsl:element name="p">
						<xsl:apply-templates select="TI/P"/>
						</xsl:element>
					</xsl:element>
                </xsl:element>
            </xsl:when>
            <xsl:when test="parent::*/parent::NP">
                <xsl:element name="alinea">
                    <xsl:attribute name="class"><xsl:value-of select="name()"/></xsl:attribute>
                    <xsl:element name="content">
						<xsl:element name="p">
						<xsl:apply-templates select="TI/P"/>
						</xsl:element>					
					</xsl:element>                
				</xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:comment>
                    <xsl:value-of select="name()"/> is a special position => not treated </xsl:comment>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!--                                                                LIST                       -->
    <!-- -->
    <xsl:template match="LIST">
        <!-- The list in an article is included in a paragraph ; the list in a paragraph or in an item is not included in another tag. in the other case, the list is included in an alinea (to validate)-->
        <xsl:choose>
            <xsl:when test="parent::*/parent::ARTICLE and preceding-sibling::*[1][self::P]">
                <xsl:element name="paragraph">
                    <xsl:apply-templates select="preceding-sibling::*[1][self::P]">
                        <xsl:with-param name="isSubparWithList" select="true()"/>
                    </xsl:apply-templates>
                    <xsl:element name="list">
                        <xsl:apply-templates/>
                    </xsl:element>
                </xsl:element>
            </xsl:when>
            <xsl:when test="parent::*/parent::ARTICLE">
                <xsl:element name="paragraph">
                    <xsl:element name="subparagraph">
                        <xsl:element name="content">
                            <xsl:element name="p"/>
                        </xsl:element>
                    </xsl:element>
                    <xsl:element name="list">
                        <xsl:apply-templates/>
                    </xsl:element>
                </xsl:element>
            </xsl:when>
            <xsl:when test="parent::*/parent::PARAG or parent::QUOT.S"> <!-- in quoted structure also -->
                <!-- 2017-05-03 - list in paragraph is not in a subparagraph -->
                <xsl:element name="list">
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="parent::TXT or parent::P">
                <xsl:element name="list">
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="ancestor::TBL | ancestor::DLIST">
                <xsl:element name="blockList">
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="alinea">
                    <xsl:element name="list">
                        <xsl:apply-templates/>
                    </xsl:element>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!-- -->
    <!--                                    TABLE in GR.TBL             -->
    <xsl:template match="GR.TBL/TBL | GR.TBL/DLIST | GR.SEQ/TBL | GR.SEQ/DLIST">
        <xsl:variable name="elementName" select="name()"/>
        <!-- TBL  :  in article is in paragraph ;  in paragraph is in subparagraph ; in the other case, is in alinea  -->
        <xsl:choose>
            <xsl:when test="parent::*/parent::*/parent::ARTICLE">
                <xsl:element name="paragraph">
                    <xsl:element name="content">
                        <xsl:element name="table">
                            <xsl:attribute name="class" select="$elementName"/>
                            <xsl:apply-templates/>
                        </xsl:element>
                    </xsl:element>
                </xsl:element>
            </xsl:when>
            <xsl:when test="parent::*/parent::*/parent::PARAG">
                <xsl:element name="subparagraph">
                    <xsl:element name="content">
                        <xsl:element name="table">
                            <xsl:attribute name="class" select="$elementName"/>
                            <xsl:apply-templates/>
                        </xsl:element>
                    </xsl:element>
                </xsl:element>
            </xsl:when>
            <xsl:when test="ancestor::DLIST | ancestor::TABLE">
                <xsl:element name="table">
                    <xsl:attribute name="class" select="$elementName"/>
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="alinea">
                    <xsl:element name="content">
                        <xsl:element name="table">
                            <xsl:attribute name="class" select="$elementName"/>
                            <xsl:apply-templates/>
                        </xsl:element>
                    </xsl:element>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!--                                                            TBL     DLIST            -->
    <xsl:template match="TBL | DLIST">
        <xsl:variable name="elementName" select="name()"/>
        <!-- TBL  :  in article is in paragraph ;  in paragraph is in subparagraph ; in the other case, is in alinea  -->
        <xsl:choose>
            <xsl:when test="parent::*/parent::ARTICLE">
                <xsl:element name="paragraph">
                    <xsl:element name="content">
                        <xsl:element name="table">
                            <xsl:attribute name="class" select="$elementName"/>
                            <xsl:apply-templates/>
                        </xsl:element>
                    </xsl:element>
                </xsl:element>
            </xsl:when>
            <xsl:when test="parent::*/parent::PARAG">
                <xsl:element name="subparagraph">
                    <xsl:element name="content">
                        <xsl:element name="table">
                            <xsl:attribute name="class" select="$elementName"/>
                            <xsl:apply-templates/>
                        </xsl:element>
                    </xsl:element>
                </xsl:element>
            </xsl:when>
            <xsl:when test="ancestor::DLIST | ancestor::TABLE">
                <xsl:element name="table">
                    <xsl:attribute name="class" select="$elementName"/>
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="alinea">
                    <xsl:element name="content">
                        <xsl:element name="table">
                            <xsl:attribute name="class" select="$elementName"/>
                            <xsl:apply-templates/>
                        </xsl:element>
                    </xsl:element>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!--                                                            FORMULA -->
    <xsl:template match="FORMULA.S">
        <xsl:choose>
            <xsl:when test="parent::*/parent::ARTICLE">
                <xsl:element name="paragraph">
                    <xsl:element name="content">
                        <xsl:element name="foreign">
                            <xsl:element name="fmx:FORMULA.S" extension-element-prefixes="fmx" namespace="http://formex.publications.europa.eu/schema/formex-05.21-20110601.xd">
                                <xsl:apply-templates mode="fmx-namespace"/>
                            </xsl:element>
                        </xsl:element>
                    </xsl:element>
                </xsl:element>
            </xsl:when>
            <xsl:when test="parent::*/parent::PARAG">
                <xsl:element name="subparagraph">
                    <xsl:element name="content">
                        <xsl:element name="foreign">
                            <xsl:element name="fmx:FORMULA.S" extension-element-prefixes="fmx" namespace="http://formex.publications.europa.eu/schema/formex-05.21-20110601.xd">
                                <xsl:apply-templates mode="fmx-namespace"/>
                            </xsl:element>
                        </xsl:element>
                    </xsl:element>
                </xsl:element>
            </xsl:when>
            <xsl:when test="ancestor::TBL | ancestor::DLIST">
                <xsl:element name="foreign">
                    <xsl:element name="fmx:FORMULA.S" extension-element-prefixes="fmx" namespace="http://formex.publications.europa.eu/schema/formex-05.21-20110601.xd">
                        <xsl:apply-templates mode="fmx-namespace"/>
                    </xsl:element>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="alinea">
                    <xsl:element name="content">
                        <xsl:element name="foreign">
                            <xsl:element name="fmx:FORMULA.S" extension-element-prefixes="fmx" namespace="http://formex.publications.europa.eu/schema/formex-05.21-20110601.xd">
                                <xsl:apply-templates mode="fmx-namespace"/>
                            </xsl:element>
                        </xsl:element>
                    </xsl:element>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!-- -->
    <xsl:template match="FORMULA">
        <xsl:element name="subFlow">
            <xsl:attribute name="name">inlineBlock</xsl:attribute>
            <xsl:element name="foreign">
                <xsl:element name="fmx:FORMULA" extension-element-prefixes="fmx" namespace="http://formex.publications.europa.eu/schema/formex-05.21-20110601.xd">
                    <xsl:apply-templates mode="fmx-namespace"/>
                </xsl:element>
            </xsl:element>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="ITEM[../@TYPE='alpha' or ../@TYPE='roman' or ../@TYPE='ARAB']">
        <xsl:choose>
            <xsl:when test="ancestor::TBL | ancestor::DLIST">
                <xsl:element name="item">
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="point">
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!-- -->
    <xsl:template match="ITEM[../@TYPE='DASH']">
        <xsl:choose>
            <xsl:when test="ancestor::TBL | ancestor::DLIST">
                <xsl:element name="item">
                    <xsl:element name="num">-</xsl:element>
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="indent">
                    <!-- à revoir -->
                    <xsl:element name="num">-</xsl:element>
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!-- -->
    <xsl:template match="ITEM[../@TYPE='NONE']">
        <xsl:choose>
            <xsl:when test="ancestor::TBL | ancestor::DLIST">
                <xsl:element name="item">
                    <xsl:element name="num">-</xsl:element>
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:element name="indent">
                    <xsl:element name="num">
                        <xsl:text> </xsl:text>
                    </xsl:element>
                    <!-- !! Leos does not accept an empty num (<num/>).  So we put a blank inside the element -->
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!-- -->
    <xsl:template match="DLIST.ITEM">
        <xsl:element name="tr">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="DLIST.ITEM/TERM">
        <xsl:element name="td">
            <xsl:element name="p">
                <xsl:element name="span">
                    <xsl:attribute name="class">TERM</xsl:attribute>
                    <xsl:apply-templates/>
                </xsl:element>
                <xsl:element name="span">
                    <xsl:attribute name="class">SEPARATOR</xsl:attribute>
                    <xsl:value-of select="parent::*/parent::*/@SEPARATOR"/>
                </xsl:element>
            </xsl:element>
        </xsl:element>
    </xsl:template>
    <xsl:template match="DLIST.ITEM/DEFINITION">
        <xsl:element name="td">
            <xsl:choose>
                <xsl:when test="not(P | LIST or FORMULA.S or TBL or DLIST)">
                    <xsl:element name="p">
                        <xsl:attribute name="class">DEFINITION</xsl:attribute>
                        <xsl:apply-templates/>
                    </xsl:element>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:element>
    </xsl:template>
    <!--  -->
    <xsl:template match="NO.P">
        <xsl:element name="num">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
	<!-- -->
	<xsl:template match="ARTICLE/ALINEA/QUOT.S">
		<xsl:element name="paragraph">
			<xsl:element name="content">
				<xsl:element name="p">
					<xsl:element name="mod">
						<xsl:element name="quotedStructure">
							<xsl:attribute name="startQuote"/>
							<xsl:attribute name="endQuote"/>
							<xsl:apply-templates/>
						</xsl:element>
					</xsl:element>
				</xsl:element>
			</xsl:element>
		</xsl:element>
	</xsl:template> 
   <!-- -->
    <xsl:template match="QUOT.S">
        <xsl:element name="mod">
            <xsl:element name="quotedStructure">
                <xsl:attribute name="startQuote"/>
                <xsl:attribute name="endQuote"/>
                <xsl:apply-templates/>
            </xsl:element>
        </xsl:element>
    </xsl:template>
    <xsl:template match="*" mode="fmx-namespace">
        <xsl:element name="fmx:{local-name()}">
            <xsl:copy-of select="@*"/>
            <xsl:apply-templates select="node()" mode="fmx-namespace"/>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="P">
        <xsl:param name = "isSubparWithList"/>
        <!-- P in alinea :  in article is paragraph or subparagraph;  in paragraph is subparagraph ; in the other case, is alinea  -->
        <xsl:choose>
            <xsl:when test="parent::*/parent::ARTICLE and following-sibling::*[1][self::LIST]">
                <xsl:if test="$isSubparWithList">
                    <xsl:element name="subparagraph">
                        <xsl:choose>
                            <xsl:when test="not(descendant::LIST or descendant::FORMULA.S or descendant::TBL or descendant::DLIST or descendant::GR.TBL or descendant::GR.SEQ) or QUOT.S">
                                <xsl:element name="content">
                                    <xsl:element name="p">
                                        <xsl:apply-templates/>
                                    </xsl:element>
                                </xsl:element>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:apply-templates/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:element>
                </xsl:if>
            </xsl:when>
            <xsl:when test="parent::*/parent::ARTICLE">
                <!-- hypothesis: ARTICLE is always composed of ALINEA or PARAG -->
                <xsl:element name="paragraph">
                    <xsl:choose>
                        <xsl:when test="not(descendant::LIST or descendant::FORMULA.S or descendant::TBL or descendant::DLIST or descendant::GR.TBL or descendant::GR.SEQ)  or QUOT.S">
                            <!-- in QUOTE.S, the substructure are in a flow element inside content -->
                            <xsl:element name="content">
                                <xsl:element name="p">
                                    <xsl:apply-templates/>
                                </xsl:element>
                            </xsl:element>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:apply-templates/>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:element>
            </xsl:when>
            <xsl:when test="parent::*/parent::PARAG">
                <!-- hypothesis: PARAG is always composed of ALINEA -->
                <xsl:element name="subparagraph">
                    <xsl:choose>
                        <xsl:when test="not(descendant::LIST or descendant::FORMULA.S or descendant::TBL or descendant::DLIST or descendant::GR.TBL or descendant::GR.SEQ) or QUOT.S">
                            <xsl:element name="content">
                                <xsl:element name="p">
                                    <xsl:apply-templates/>
                                </xsl:element>
                            </xsl:element>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:apply-templates/>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:element>
            </xsl:when>
            <xsl:when test="parent::NP and not(LIST or FORMULA.S or TBL or DLIST or GR.TBL or GR.SEQ) and ancestor::ENACTING.TERMS">
				<!-- P in NP or in QUOT.S is always a second block -->
				<xsl:element name="alinea">
					<xsl:element name="content">
						<xsl:element name="p">
							<xsl:apply-templates/>
						</xsl:element>
					</xsl:element>
				</xsl:element>
            </xsl:when>
            <xsl:when test="(parent::NP) and LIST or FORMULA.S or TBL or DLIST or GR.TBL or GR.SEQ and ancestor::ENACTING.TERMS">
                <xsl:apply-templates/>
            </xsl:when>
            <xsl:when test="parent::FINAL">
                <xsl:element name="clause">
                    <xsl:element name="content">
                        <xsl:element name="p">
                            <xsl:apply-templates/>
                        </xsl:element>
                    </xsl:element>
                </xsl:element>
            </xsl:when>
 			<xsl:when test="parent::QUOT.S and ancestor::ENACTING.TERMS">
				<!-- P as child of QUOT.S is always a block inside a point / indent -->
				<xsl:element name="alinea">
					<xsl:element name="content">
						<xsl:element name="p">
							<xsl:apply-templates/>
						</xsl:element>
					</xsl:element>
				</xsl:element>
			</xsl:when>
           <xsl:when test="parent::PL.DATE">
                <xsl:element name="p">
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:when>
            <xsl:when test="parent::SIGNATORY">
                <xsl:choose>
                    <xsl:when test="position()=1">
                        <xsl:element name="organization">
                            <xsl:attribute name="refersTo"/>
                            <xsl:apply-templates/>
                        </xsl:element>
                    </xsl:when>
                    <xsl:when test="position()=2">
                        <xsl:element name="role">
                            <xsl:attribute name="refersTo"/>
                            <xsl:apply-templates/>
                        </xsl:element>
                    </xsl:when>
                    <xsl:when test="position()=3">
                        <xsl:element name="person">
                            <xsl:attribute name="refersTo"/>
                            <xsl:apply-templates/>
                        </xsl:element>
                    </xsl:when>
                    <xsl:otherwise>
  						<xsl:text disable-output-escaping="yes">&lt;!-- &lt;leos:unknown></xsl:text>
						<xsl:copy-of select="." exclude-result-prefixes="#all" /><xsl:text disable-output-escaping="yes">&lt;/leo:unknown> --></xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:when>
			<xsl:when  test="parent::NOTE">
				<xsl:element name="p">
					<xsl:apply-templates/>
				</xsl:element>
			</xsl:when>
 			<xsl:when test="ancestor::CONSID"> <!-- only one p in recital -->
				<xsl:text> </xsl:text><xsl:apply-templates/>
			</xsl:when>				
           <xsl:otherwise>
                <xsl:element name="p">
                    <xsl:if test="not(parent::NOTE or parent::CELL or parent::TI or parent::DEFINITION)">
                        <xsl:comment>default P | TXT </xsl:comment>
                    </xsl:if>
                    <xsl:apply-templates/>
                </xsl:element>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!-- -->
    <xsl:template match="TBL/CORPUS">
        <xsl:apply-templates/>
    </xsl:template>
    <!-- -->
    <xsl:template match="ROW">
        <xsl:element name="tr">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="ROW[@TYPE='HEADER']/CELL">
        <xsl:element name="th">
            <xsl:choose>
                <xsl:when test="not(P or LIST or FORMULA.S or TBL or DLIST)">
                    <xsl:element name="p">
                        <xsl:apply-templates/>
                    </xsl:element>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="CELL">
        <xsl:element name="td">
            <xsl:if test="@ROWSPAN">
                <xsl:attribute name="rowspan" select="@ROWSPAN"/>
            </xsl:if>
            <xsl:choose>
                <xsl:when test="not(P or LIST or FORMULA.S or TBL or DLIST)">
                    <xsl:element name="p">
                        <xsl:apply-templates/>
                    </xsl:element>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="FINAL/SIGNATURE">
        <xsl:element name="conclusions">
            <xsl:apply-templates select="PL.DATE"/>
            <xsl:if test="SIGNATORY">
                <xsl:element name="block">
                    <xsl:attribute name="name">signatory</xsl:attribute>
                    <xsl:apply-templates select="SIGNATORY"/>
                </xsl:element>
            </xsl:if>
            <xsl:for-each select="*[not(name()='PL.DATE' or name()='SIGNATORY')]">
 				<xsl:comment>&lt;leos:unknown><xsl:copy-of select="."/>&lt;/leo:unknown></xsl:comment>
            </xsl:for-each>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="SIGNATURE/PL.DATE">
        <xsl:apply-templates/>
    </xsl:template>
    <!-- -->
    <xsl:template match="SIGNATURE/SIGNATORY">
        <xsl:element name="signature">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="comment()| processing-instruction()" mode="fmx-namespace">
        <xsl:copy/>
    </xsl:template>
    <xsl:template match="HT[@TYPE='ITALIC']">
		<xsl:choose>
			<xsl:when test="ancestor::TI or ancestor::STI or ancestor::SIGNATORY"><xsl:apply-templates/></xsl:when>
			<xsl:otherwise>
				<xsl:element name="i">
					<xsl:apply-templates/>
				</xsl:element>
			</xsl:otherwise>
		</xsl:choose>
    </xsl:template>
	<!-- -->
	<xsl:template match="HT[@TYPE='BOLD']">
		<xsl:choose>
			<xsl:when test="ancestor::TI or ancestor::STI or ancestor::SIGNATORY"><xsl:apply-templates/></xsl:when>
			<xsl:otherwise>
				<xsl:element name="b">
					<xsl:apply-templates/>
				</xsl:element>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
    <!-- -->
    <xsl:template match="HT[@TYPE='SUB']">
        <xsl:element name="sub">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <!-- -->
    <xsl:template match="HT[@TYPE='UC']">
        <xsl:value-of select="upper-case(.)"/>
    </xsl:template>
    <!-- -->
    <xsl:template match="HT[@TYPE='SUP']">
        <xsl:element name="sup">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="QUOT.START">
        <xsl:choose>
            <xsl:when test="@CODE='2018' cast as xs:hexBinary">
                <xsl:text>‘</xsl:text>
            </xsl:when>
 			<xsl:when test="@CODE='201C' cast as xs:hexBinary">
				<xsl:text>“</xsl:text>
			</xsl:when>			
           <xsl:when test="@CODE='0022' cast as xs:hexBinary">
                <xsl:text>"</xsl:text>
            </xsl:when>
            <xsl:when test="@CODE='0027' cast as xs:hexBinary">
                <xsl:text>'</xsl:text>
            </xsl:when>
            <xsl:otherwise>
				<xsl:text disable-output-escaping="yes">&lt;!-- &lt;leos:unknown></xsl:text>
				<xsl:copy-of select="." exclude-result-prefixes="#all" /><xsl:text disable-output-escaping="yes">&lt;/leo:unknown> --></xsl:text>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="QUOT.END">
        <xsl:choose>
            <xsl:when test="@CODE='2019'  cast as xs:hexBinary">
                <xsl:text>’</xsl:text>
            </xsl:when>
 			<xsl:when test="@CODE='201D' cast as xs:hexBinary">
				<xsl:text>”</xsl:text>
			</xsl:when>
           <xsl:when test="@CODE='0022' cast as xs:hexBinary">
                <xsl:text>"</xsl:text>
            </xsl:when>
            <xsl:when test="@CODE='0027' cast as xs:hexBinary">
                <xsl:text>'</xsl:text>
            </xsl:when>
            <xsl:otherwise>
				<xsl:text disable-output-escaping="yes">&lt;!-- &lt;leos:unknown></xsl:text>
				<xsl:copy-of select="." exclude-result-prefixes="#all" /><xsl:text disable-output-escaping="yes">&lt;/leo:unknown> --></xsl:text>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <!-- -->
    <xsl:template match="REF.DOC.OJ | DATE | FT[@TYPE='NUMBER'  or @TYPE='DECIMAL']  | FT[@TYPE='CN'] ">
        <xsl:apply-templates/>
    </xsl:template>
    <!-- -->

    <!-- not treated -->
    <xsl:template match="TOC"/>
    <!-- -->
    <!-- by default  -->
    <xsl:template match="*">
        <xsl:if test="name()='HT' and not(ancestor::TI or ancestor::STI)">
            <xsl:comment>!!! <xsl:value-of select="name()"/> is implicitely treated !!!</xsl:comment>
        </xsl:if>
        <xsl:apply-templates/>
    </xsl:template>
</xsl:stylesheet>
