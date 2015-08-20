#!/usr/bin/env perl

use Mojolicious::Lite;
use DBI;
use DBD::mysql;

# Create a database connection as an application attribute
app->attr(dbh => sub {
    my $self = shift;
    
    my $dbh = DBI->connect(
    'DBI:mysql:FlyAtlasDB:127.0.0.1:3306','root','spider'
    ) or die "Unable to connect: $DBI::errstr\n";
    
    return $dbh;
});

get '/' => sub {
    my $self = shift;
    $self->render('index');
};

get '/results' => sub {
    my $self = shift;
    my $gene = $self->param('gene');
    
   # my $query = q(
   #     SELECT DISTINCT Gene.FBgn, Gene.CGNum, Gene.Symbol, Gene.Name,
   #             Experiment.ProbesetID, Experiment.SignifChange, Experiment.Abundance, Experiment.AbundanceSE,
   #             Experiment.SignalDetected, Experiment.Enrichment, Experiment.FlyID,
   #             Probeset.ProbeDegeneracy
   #     FROM Experiment, Probeset, Gene
   #     WHERE Gene.FBgn = Probeset.FBgn
   #     AND Probeset.ProbesetID = Experiment.ProbesetID
   #     AND (Gene.Name = ? OR Gene.RomanName = ? ) 
   #     ORDER BY Probeset.FBgn, Experiment.ProbesetID, Experiment.FlyID
   # );

    my $query = q(SELECT * FROM Gene WHERE Gene.Name = ?);
    
    my $dbh = $self->app->dbh;
    my $sth = $dbh->prepare($query);
    
    $sth->execute($gene);
    
    $self->stash(
        gene => $gene,
        query => $query,
        results => $sth->fetchall_arrayref()
    );
    
    $self->render('results');
};

app->start;

__DATA__

@@ layouts/default.html.ep
<!DOCTYPE html>
<html>
    <head>
        <title><%= title %></title>

        #Header#
        <table width="100%" border=0 cellpadding="1">
            <tr>
                <td width="150"><img src="flyatlas_logo.jpg" alt="Flyatlas logo" width="150" height="151"></td>
                <td ><h1 align="center"><font color="#000099" size="5" face="Arial, Helvetica, sans-serif">FlyAtlas: the <i>Drosophila</i> gene expression atlas</font></h1></td>
                <td width="150"><a href="http://www.gla.ac.uk"><img src="crest.gif" alt="University of Glasgow" width=200 height="76"></a><br>
     
                <a href="http://www.bbsrc.ac.uk"/><img src="bbsrcsmallcolour.gif" alt="Biotechnology &amp; Biological Sciences Research Council" width=200 height="76"></a></td>
            </tr>
        </table>
        
        #Navigation bar will change with bootstrap#
        <div>
        <table width="100%" border="1" cellpadding="2">
            <tr> 
                <td><div align="center"><strong><font color="#0033FF" size="1" face="Arial, Helvetica, sans-serif"><a href="atlas.cgi">Home &amp; Search</a></font></strong></div></td>
                <td><div align="center"><strong><font color="#0033FF" size="1" face="Arial, Helvetica, sans-serif"><a href="batch_table.cgi">Batch/table Search</a></font></strong></div></td>
                <td><div align="center"><strong><font color="#0033FF" size="1" face="Arial, Helvetica, sans-serif"><a href="tissues.cgi">Tissues Search</a></font></strong></div></td>
                <td><div align="center"><strong><font color="#0033FF" size="1" face="Arial, Helvetica, sans-serif"><a href="blast.cgi">BLASTP Search</a></font></strong></div></td>
                <td><div align="center"><strong><font color="#0033FF" size="1" face="Arial, Helvetica, sans-serif"><a href="about_atlas.html">About & FAQ</a></font></strong></div></td>
                <td><div align="center"><strong><font color="#0033FF" size="1" face="Arial, Helvetica, sans-serif"><a href="top50.html">Top 50</a></font></strong></div></td>
                <td><div align="center"><strong><font color="#0033FF" size="1" face="Arial, Helvetica, sans-serif"><a href="data.html">Original data</a></font></strong></div></td>
                <td><div align="center"><strong><font color="#0033FF" size="1" face="Arial, Helvetica, sans-serif"><a href="meta/equation.html">Interesting meta-analysis</a></font></strong></div></td>
                <td><div align="center"><strong><font color="#0033FF" size="1" face="Arial, Helvetica, sans-serif"><a href="links.html">Links</a></font></strong></div></td>
            </tr>
        </table>
        </div>
    </head>
    <body>
        <%= content %>
        <div>
        <br><br><br>Chintapalli, V. R., Wang, J. and Dow, J. A. T. (2007). Using FlyAtlas to identify better Drosophila models of human disease. <a href=http://www.nature.com/ng/journal/v39/n6/abs/ng2049.html target=_blank><i>Nature Genetics</i> 39: 715-720</a>
        </div>
    </body>
</html>

@@ index.html.ep
% layout 'default';
% title 'FlyAtlas: the Drosophila expression atlas';
<h1> Basic Web Form Example</h1>
<p>
    Please enter a gene name and click 'Search' to get a report of information for a gene.
</p>
<p>
    (If you are at loss for something to search for, try <strong>p53</strong> or <strong>ATP%</strong>).
</p>

<form method = "get" action = "/results">
    <p>
        Gene:
        <input type = "text" name = "gene" size = "15" />
        <input type = "submit" value = "Search" />
        <input type = "reset" value = "Clear" />
    </p>
</form>

@@ results.html.ep
% layout 'default';
% title "Search results For: '$gene'";
<h1> Search results for: '<%= $gene %>'</h1>
<p>
    The table below was created by running this query on the 'homo_sapiens_core' database at <a href="http://www.ensembl.org"> Ensembl</a>
</p>

<pre><%= $query %></pre>
<table border = "1" cellpadding = "3" cellspacing = "3">
    <thead>
        <tr>
            <th> External synonym </th>
            <th> Seq Region Name </th>
            <th> Seq Region Start </th>
            <th> Seq Region End </th>
        </tr>
    </thead>
    <tbody>
    <% foreach my $result (@{$results}) { %>
        <tr>
        <% foreach my $item (@{$result}) { %>
            <td><%= $item %></td>
            <% } %>
        </tr>
        <% } %>
    </tbody>
</table>
