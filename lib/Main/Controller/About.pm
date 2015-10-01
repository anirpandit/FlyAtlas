# Controller
package Main::Controller::About;
use Mojo::Base 'Mojolicious::Controller';

# Action
sub get_credits {
    
    my $self = shift;
    $self->render('/about/credits');
}

sub get_datasetinfo {
    
    my $self = shift;
	
	my $dbh = $self->app->dbh;
    
    my $query = '
    SELECT DISTINCT TissueName, TissueDefinition
    FROM TissueInformation' ;
    
    my $sth = $dbh->prepare($query);
    $sth->execute();

    $self->stash(
    	tissueinfo => $sth->fetchall_arrayref,
    );

    $self->render('/about/datasetinfo');
}

sub get_faq {
    
    my $self = shift;
    $self->render('/about/FAQ');
}

sub get_originaldata {
    
    my $self = shift;
    $self->render('/about/originaldata');
}

1;