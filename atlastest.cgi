#!c:/perl/bin/perl.exe
#Atlas v 0.1
#JATD 9/4/07
#***places to add code for new tissues are marked like this***

use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
include "settings.txt";
include "routines.txt";

&do_headers;
&do_form;

if (param()) {
   $search=param('name');
   print "<hr>";

if (length($search)>2) {
	$s=uc($search);
	$t=time;
	&read_homophila;
	&read_biogrid;
	&read_insitu;
	&read_array;
	&read_wien;
	&search_annot;
	&output;
	$elapsed=time-$t;
}
print "Looking for $search. $match entries matched from $n, in $elapsed s. \n",p;
}
&do_footer;

