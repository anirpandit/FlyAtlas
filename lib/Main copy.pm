package Main;
use Mojo::Base 'Mojolicious';

use DBI;
use DBD::mysql;

use Main::Model::Users;

sub startup {
	my $self = shift;

    (ref $self)->attr(
        dbh => sub {
            DBI->connect(
    		'DBI:mysql:FlyAtlasDB:127.0.0.1:3306','root','spider'
    		);
        }
    );

	#For Hypnotoad, config file call#
	my $config = $self->plugin('Config');
    
    
    $self->secrets(['Mojolicious rocks']);
    $self->helper(users => sub { state $users = Main::Model::Users->new });

	#For Routes#
	my $r = $self->routes;


	#Routes to Controllers#

	$r -> get('/') -> to(controller => 'sitepages', action => 'go_home');
	$r -> get('/home') -> to(controller => 'sitepages', action => 'go_home');


   	$r -> get('/microarraydata/genesearch') -> to(controller => 'genesearch', action => 'do_genesearch');
        $r -> get('/microarraydata/externallinks') -> to(controller => 'genesearch', action => 'get_extlinks');
    $r -> get('/microarraydata/tissuesearch') -> to(controller => 'microarraydata', action => 'do_tissuesearch');
    $r -> get('/microarraydata/blastp') -> to(controller => 'microarraydata', action => 'do_blastp');
    
    $r -> get('/about/credits') -> to(controller => 'about', action => 'get_credits');
    $r -> get('/about/datasetinfo') -> to(controller => 'about', action => 'get_datasetinfo');

    $r -> get('/contactus') -> to(controller => 'sitepages', action => 'get_contact');

    #Login Routes#
    $r->get('/login')->to('login#login')->name('login');
    
    my $logged_in = $r->under('/')->to('login#logged_in');
    $logged_in->get('/datamgmt')->to('login#datamgmt');
    
    $r->get('/logout')->to('login#logout');
}

1;