# Controller
package Main::Controller::Genesubs;
use Main;

require Exporter;
  my @ISA = qw(Exporter);


    my $dbh = DBI->connect('DBI:mysql:FlyAtlasDB:127.0.0.1:3306','root','spider') or die "Could not connect";

sub headervalues{

    my $FBgn = shift;

    my $query = q(
            SELECT DISTINCT Gene.Name, Gene.Symbol, Gene.CGNum, Gene.FBgn, Experiment.ProbesetID
            FROM Gene, Experiment, Probeset
            WHERE Gene.FBgn = Probeset.FBgn
            AND Probeset.ProbesetID = Experiment.ProbesetID
            AND Gene.FBgn = ?
        );

    my $sth = $dbh->prepare($query);
    
    $sth->execute($FBgn);

    my $headervalues = $sth->fetchall_arrayref;

    return ($headervalues);
}

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