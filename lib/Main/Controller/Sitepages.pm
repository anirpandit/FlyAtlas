# Controller
package Main::Controller::Sitepages;
use Mojo::Base 'Mojolicious::Controller';

# Action
sub go_home {
    
    my $self = shift;
    $self->render('/home');
}

sub get_contact {
    
    my $self = shift;
    $self->render('/contact');
}

1;