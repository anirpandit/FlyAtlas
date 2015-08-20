#!/usr/bin/env perl
use Mojolicious::Lite;

# Documentation browser under "/perldoc"
plugin 'PODRenderer';

get '/' => sub {
  my $c = shift;
  $c->render(template => 'index');
};

my $content="I am starting to like tis Mojocrapilicious";

app->start;
__DATA__

@@ index.html.ep
% layout 'default';
% title 'FlyAtlas: the Drosophila expression atlas';


@@ layouts/default.html.ep
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title><%= title %></title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<meta name="Description" lang="en" content="Affymetrix-derived atlas of gene expression in multiple Drosophila tissues">
<meta name="Keywords" lang="en" content="Drosophila melanogaster microarray transcriptome transcriptomics brain head midgut hindgut Malpighian tubule fat body thoracicoabdominal ganglion ovary testis accessory gland spermatheca  salivary gland Julian Dow">
<meta name="Robots" content="Index, Follow">
<meta name="Revisit-After" content="14 days">

<meta name="Owner" content="Julian Dow">
<meta name="Rating" content="General">
<meta name="Distribution" content="Global">
<meta name="Language" content="en">
<meta name="Title" content="FlyAtlas">
<meta http-equiv="Page-Enter" content="blendTrans(Duration=1.0)">
<style type="text/css">
h1 {color:blue;}
p {font:"Arial";}
</style>
</head>
<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
try {
    var pageTracker = _gat._getTracker("UA-8068861-1");
    pageTracker._trackPageview();
} catch(err) {}</script>
<body>
<table width="100%" border=0 cellpadding="1">
<tr>
<td width="150"><img src="~/flyatlas_logo.jpg" alt="Flyatlas logo" width="150" height="151"></td>
<td ><h1 align="center"><font color="#000099" size="5" face="Arial, Helvetica, sans-serif">FlyAtlas:
the <i>Drosophila</i> gene expression atlas</font></h1></td>
<td width="150"><a href=http://www.gla.ac.uk/><img src=crest.gif alt="University of Glasgow" width=200 height="76"></a><br>

<a href=http://www.bbsrc.ac.uk/><img src=bbsrcsmallcolour.gif alt="Biotechnology &amp; Biological Sciences Research Council" width=200 height="76"></a></td>
</tr></table>
<table width="100%" border="1" cellpadding="2">
<tr>
<td><div align="center"><strong><font color="#0033FF" size="1" face="Arial, Helvetica, sans-serif"><a href="atlas.cgi">Home
&amp; Search</a></font></strong></div></td>
<td><div align="center"><strong><font color="#0033FF" size="1" face="Arial, Helvetica, sans-serif"><a href="batch_table.cgi">Batch/table
Search</a></font></strong></div></td>
<td><div align="center"><strong><font color="#0033FF" size="1" face="Arial, Helvetica, sans-serif"><a href="tissues.cgi">Tissues
Search</a></font></strong></div></td>
<td><div align="center"><strong><font color="#0033FF" size="1" face="Arial, Helvetica, sans-serif"><a href="blast.cgi">BLASTP
Search</a></font></strong></div></td>
<td><div align="center"><strong><font color="#0033FF" size="1" face="Arial, Helvetica, sans-serif"><a href="about_atlas.html">About
& FAQ</a></font></strong></div></td>
<td><div align="center"><strong><font color="#0033FF" size="1" face="Arial, Helvetica, sans-serif"><a href="top50.html">Top
50</a></font></strong></div></td>
<td><div align="center"><strong><font color="#0033FF" size="1" face="Arial, Helvetica, sans-serif"><a href="data.html">Original
data</a></font></strong></div></td>
<td><div align="center"><strong><font color="#0033FF" size="1" face="Arial, Helvetica, sans-serif"><a href="meta/equation.html">Interesting
meta-analysis</a></font></strong></div></td>
<td><div align="center"><strong><font color="#0033FF" size="1" face="Arial, Helvetica, sans-serif"><a href="links.html">Links</a></font></strong></div></td>

</tr>
</table>
</head>
<body><%= content %></body>
</html>

