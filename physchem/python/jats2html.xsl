<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="*">
        <xsl:text>UNKNOWN-TAG: </xsl:text><xsl:value-of select="name()"/>
    </xsl:template>
    <xsl:template match="italic">
        <i><xsl:apply-templates/></i>
    </xsl:template>
    <xsl:template match="p|sec|title">
        <xsl:copy select="name()|@*"><xsl:apply-templates/></xsl:copy>
    </xsl:template>
    <xsl:template match="ack">
        <div type="{name()}"><xsl:apply-templates/></div>
    </xsl:template>
    <xsl:template match="xref">
        <a href="{@rid}"><xsl:text>[</xsl:text><xsl:value-of select="."/><xsl:text>]</xsl:text></a>
    </xsl:template>
</xsl:stylesheet>