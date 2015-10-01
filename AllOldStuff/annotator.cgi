#!c:/perl/bin/perl.exe
#annotate v 0.1
#JATD 16/8/07
#***places to add code for new tissues are marked like this***

use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
$ua = $ENV{REMOTE_ADDR};
$annot_file="Drosophila_2.na23.annot.csv";
$array_file="all.txt";

print header('text/plain');
#print start_html('The Drosophila adult expression atlas');
	&read_annot;
	&read_array;
	&output;
print end_html;

sub read_annot {
#readaffy annotation file data
open(ANNOT,"<$annot_file") || die "Cant get $annot_file file";
#read in the data file

while (<ANNOT>) {
   $n++;
   chomp();
#   $_=~s/([0-9]), ([0-9])/$1 $2/g;
   $_=~s/---//g;
#   $_=~s/,/\t/g;
#   $_=~s/\"//g;
   $_=~s/\",\"/\t/g;
		if ($_=~/([0-9]+_[_astx]+)/ )   {
			$oligo=$1;
			$array{$oligo}=$_;
			}
	}
	   close ANNOT;
}

sub read_array {
#read aa data
open(ARRAY,"<$array_file") || die "Cant get $array_file file";
$ar=0;
#read in the data file
while (<ARRAY>) {
   chomp();
   $ar++;
   if ($ar == 1) {
      print "$_\n";
      }
   
		if ($_=~/([0-9]+_[_astx]+)/ )   {
			$oligo=$1;
      print "$_\t$array{$oligo}\n";
	    }	
   }
	close ARRAY;
}

