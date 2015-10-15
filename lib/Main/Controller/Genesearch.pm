# Controller
package Main::Controller::Genesearch;
use Mojo::Base 'Mojolicious::Controller';

require Exporter;
  my @ISA = qw(Exporter);


#Gene Search Form route#
sub do_genesearch {

    my $self = shift;
    my $gene = $self->param('gene');

    my $searchtype= $self->param('searchtype');

    #Gene Search Form Queries#
    my ($query);

    if(defined $searchtype == 1){
        $query = q(
            SELECT DISTINCT Gene.FBgn 
            FROM Gene
            WHERE Gene.Name = ? 
        );
    }

    elsif(defined $searchtype == 2){
        $query = q(
            SELECT DISTINCT Gene.FBgn 
            FROM Gene
            WHERE Gene.Symbol = ? 
        );
    }

    elsif(defined $searchtype == 3){
        $query = q(
            SELECT DISTINCT Gene.FBgn 
            FROM Gene
            WHERE Gene.CGNum = ?
        );
    }

    else{
        $query = q(
            SELECT DISTINCT Gene.FBgn 
            FROM Gene
            WHERE Gene.FBgn = ?
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

sub headervalues{
    
    my $self = shift;
    my $FBgn = shift;

    my $query = q(
            SELECT DISTINCT Gene.Name, Gene.Symbol, 
            Gene.CGNum, Gene.FBgn, Experiment.ProbesetID, 
            FROM Experiment, Probeset, Gene, FlyAnat
            WHERE Gene.FBgn = Probeset.FBgn
            AND Probeset.ProbesetID = Experiment.ProbesetID
            AND Gene.FBgn = ? 
        );


    my $dbh = $self->app->dbh;
    my $sth = $dbh->prepare($query);
    
    $sth->execute($FBgn);

    my @headervalues=$sth->fetchall_arrayref;

    return @headervalues;
}
1;