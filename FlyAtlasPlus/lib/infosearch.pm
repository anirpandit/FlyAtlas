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

#Gene Search Form route#
get '/genesearch' => sub {
    my $self = shift;
    my $gene = $self->param('gene');
    my $searchtype= $self->param('searchtype');

    #Gene Search Form Queries#
    my ($query);
    if($searchtype == 1){
        $query = q(

            SELECT DISTINCT Gene.Name, Gene.Symbol, 
            Gene.CGNum, Gene.FBgn, Experiment.ProbesetID, 
            FlyAnat.UniTissue,Experiment.FlyID,
            Experiment.SignifChange, Experiment.Abundance, Experiment.AbundanceSE,
            Experiment.SignalDetected, Experiment.Enrichment, 
            Probeset.ProbeDegeneracy
            FROM Experiment, Probeset, Gene, FlyAnat
            WHERE Gene.FBgn = Probeset.FBgn
            AND Probeset.ProbesetID = Experiment.ProbesetID
            AND FlyAnat.FlyID = Experiment.FlyID
            AND (Gene.Symbol = BINARY ?)
            ORDER BY Probeset.FBgn, Experiment.ProbesetID, Experiment.FlyID 
        );
    }

    elsif($searchtype == 2){
        $query = q(
            SELECT DISTINCT Gene.Name, Gene.Symbol, 
            Gene.CGNum, Gene.FBgn, Experiment.ProbesetID, 
            FlyAnat.UniTissue,Experiment.FlyID,
            Experiment.SignifChange, Experiment.Abundance, Experiment.AbundanceSE,
            Experiment.SignalDetected, Experiment.Enrichment, 
            Probeset.ProbeDegeneracy
            FROM Experiment, Probeset, Gene, FlyAnat
            WHERE Gene.FBgn = Probeset.FBgn
            AND Probeset.ProbesetID = Experiment.ProbesetID
            AND FlyAnat.FlyID = Experiment.FlyID
            AND (Gene.Name = ? ) 
            ORDER BY Probeset.FBgn, Experiment.ProbesetID, Experiment.FlyID
        );
    }

    elsif($searchtype == 3){
        $query = q(
            SELECT DISTINCT Gene.Name, Gene.Symbol, 
            Gene.CGNum, Gene.FBgn, Experiment.ProbesetID, 
            FlyAnat.UniTissue,Experiment.FlyID,
            Experiment.SignifChange, Experiment.Abundance, Experiment.AbundanceSE,
            Experiment.SignalDetected, Experiment.Enrichment, 
            Probeset.ProbeDegeneracy
            FROM Experiment, Probeset, Gene, FlyAnat
            WHERE Gene.FBgn = Probeset.FBgn
            AND Probeset.ProbesetID = Experiment.ProbesetID
            AND FlyAnat.FlyID = Experiment.FlyID
            AND Gene.CGNum = ?
            ORDER BY Probeset.FBgn, Experiment.ProbesetID, Experiment.FlyID
        );
    }

    else{
        $query = q(
            SELECT DISTINCT Gene.Name, Gene.Symbol, 
            Gene.CGNum, Gene.FBgn, Experiment.ProbesetID, 
            FlyAnat.UniTissue,Experiment.FlyID,
            Experiment.SignifChange, Experiment.Abundance, Experiment.AbundanceSE,
            Experiment.SignalDetected, Experiment.Enrichment, 
            Probeset.ProbeDegeneracy
            FROM Experiment, Probeset, Gene, FlyAnat
            WHERE Gene.FBgn = Probeset.FBgn
            AND Probeset.ProbesetID = Experiment.ProbesetID
            AND FlyAnat.FlyID = Experiment.FlyID
            AND Gene.FBgn = ?
            ORDER BY Probeset.FBgn, Experiment.ProbesetID, Experiment.FlyID
        );
    }
    
    my $dbh = $self->app->dbh;
    my $sth = $dbh->prepare($query);
    
    $sth->execute($gene);
    
    $self->stash(
        gene => $gene,
        query => $query,
        results => $sth->fetchall_arrayref
    );
    
    $self->render('genesearch');
};

