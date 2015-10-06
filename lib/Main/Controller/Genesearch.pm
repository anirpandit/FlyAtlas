# Controller
package Main::Controller::Genesearch;
use Mojo::Base 'Mojolicious::Controller';


#Gene Search Form route#
sub do_genesearch {

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
        results => $sth->fetchall_arrayref
    );
    
    $self->render('/microarraydata/genesearch');
};


1;