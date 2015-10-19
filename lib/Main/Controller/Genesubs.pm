# Controller
package Main::Controller::Genesubs;
use Main;

require Exporter;
  my @ISA = qw(Exporter);


    my $dbh = DBI->connect('DBI:mysql:FlyAtlasDB:127.0.0.1:3306','root','spider') or die "Could not connect";

sub getgenedata{

    my $FBgn = shift;
    my $ProbesetID = shift;

    my $query = q(
            SELECT DISTINCT 
            FlyAnat.UniTissue,Experiment.FlyID,
            Experiment.SignifChange, Experiment.Abundance, Experiment.AbundanceSE,
            Experiment.SignalDetected, Experiment.Enrichment, 
            Probeset.ProbeDegeneracy
            FROM Experiment, Probeset, Gene, FlyAnat
            WHERE Gene.FBgn = Probeset.FBgn
            AND Probeset.ProbesetID = Experiment.ProbesetID
            AND FlyAnat.FlyID = Experiment.FlyID
            AND (Gene.FBgn = ? AND Probeset.ProbesetID = ?)
            ORDER BY Probeset.FBgn, Experiment.ProbesetID, Experiment.FlyID 
        );

    my $sth = $dbh->prepare($query);
    
    $sth->execute($FBgn,$ProbesetID);

    my $genedata = $sth->fetchall_arrayref;

    return $genedata;  

}
1;