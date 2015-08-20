#!c:/perl/bin/perl.exe
#batch table
#JATD 18/5/07
#***places to add code for new tissues are marked like this***

use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
$ua = $ENV{REMOTE_ADDR};
	$annot_file="Drosophila_2.na23.annot.csv";
	$array_file="all.txt";
	$maxhits=100;

&do_headers;

&do_form;
if (param()) {
#   &read_homophila;
#	&read_insitu;
	$t=time;
print "<font size=-1><table border=1>";
#***places to add code for new tissues are marked like this***
print "<tr><td>oligo</td><td>brainMean</td><td>headMean</td><td>tagMean</td><td>sgMean</td><td>cropMean</td><td>midgutMean</td><td>tubuleMean</td><td>hindgutMean</td><td>ovaryMean</td><td>testisMean</td><td>accMean</td><td>carMean</td><td>l_tubMean</td><td>l_fatMean</td><td>flyMean</td><td>description</td></tr>";
   $search=param('name');
   print "<hr>";
$s=uc($search);
@lines = split (/\n/,$s);
foreach (@lines) {
chomp;
   $s=uc($_);
   $s =~s/^[\s]+//;
   $s =~s/[\s]+$//;
$m=0;
if (length($s)>2) {
#   print "Looking for: $s.<p>\n";
	&search_annot;
} else {
print "Search string too short!",p;
}
}
	&pull_data;
}
print "</table></font>";
# print "Looking for $search. $match entries matched from $n, in $elapsed s. Read $m lines from array file, and matched $arraymatch.\n",p;
	$elapsed=time-$t;

sub do_headers {
print "content-type: text/html \n\n"; #The header

$HTML = "heading.html";
open (HTML) or die "Can't open the file!";
print <HTML>;
close (HTML);
  
#***places to add code for new tissues are marked like this***
open(INFILE,"news.txt") || die "Cant get newsfile";
while (<INFILE>) {
   chomp;
   print "<b>Latest news</b>: $_",br;
   }
close INFILE;
 print p,hr;  
$HTML = "description.html";
open (HTML) or die "Can't open the file!";
print <HTML>;
close (HTML);
}

sub do_form {
print "This is the batch search page. Enter one search term per line:<br>";
print	start_form,textarea('name','',20,20), submit,br,
    "e.g. vha, cell adhesion, receptor, aquaporin, adenylate, CG1147, pnt", p,
" If you don\'t get a hit for a particular gene, look it up ",
" in Flybase and try any synonyms (FBgn number, CG number, etc)",p;

    end_form,
    hr;
print end_html;
}

sub search_annot {
#readaffy annotation file data
open(INFILE,"<$annot_file") || die "Cant get $annot_file file";
#read in the data file
$n=0;
$match=0;
#   print "Looking for: $s.<p>\n";

while (<INFILE>) {
   $n++;
   chomp();
   $_=~s/---//g;
   $_=~s/\",\"/\t/g;
$ST=uc($_);
    if ($ST =~ /$s/) {
		$match++;
#		print "Match for $s.",br;
		if ($_=~/([0-9]+_[_astx]+)/ )   {
			$oligo=$1;
#			print "$oligo",br;
			$hits{$oligo}=$_;
			}
	}
	if ($match > $maxhits) {
	   print "You got more than $maxhits hits. Just showing the first $maxhits.\n";
	   close INFILE;
	   last;
	   }
	if ($ST =~ /AFFYMETRIX/) {
	   close INFILE;
	   last;
	   }
}
close INFILE;
print "Searching for $s through $n annotations produced $match hits",p;
}	

sub pull_data {
#read aa data
open(INFILE,"<$array_file") || die "Cant get $array_file file";
#read in the data file
$m=0;
$arraymatch=0;

while (<INFILE>) {
   $m++;
   chomp();
   ($oli,
   $brain_fly_t,$brainMean,$brainSEM,$brainCall,$brainRatio,
   $head_fly_t,$headMean,$headSEM,$headCall,$headRatio,
   $crop_fly_t,$cropMean,$cropSEM,$cropCall,$cropRatio,
   $midgut_fly_t,$midgutMean,$midgutSEM,$midgutCall,$midgutRatio,
   $hindgut_fly_t,$hindgutMean,$hindgutSEM,$hindgutCall,$hindgutRatio,
   $tubule_fly_t,$tubuleMean,$tubuleSEM,$tubuleCall,$tubuleRatio,
   $ovary_fly_t,$ovaryMean,$ovarySEM,$ovaryCall,$ovaryRatio,
   $testis_fly_t,$testisMean,$testisSEM,$testisCall,$testisRatio,
   $acc_fly_t,$accMean,$accSEM,$accCall,$accRatio,
   $l_tub_fly_t,$l_tubMean,$l_tubSEM,$l_tubCall,$l_tubRatio,
   $l_fat_fly_t,$l_fatMean,$l_fatSEM,$l_fatCall,$l_fatRatio,
   $tag_fly_t,$tagMean,$tagSEM,$tagCall,$tagRatio,
   $car_fly_t,$carMean,$carSEM,$carCall,$carRatio,
   $sg_fly_t,$sgMean,$sgSEM,$sgCall,$sgRatio,
#***places to add code for new tissues are marked like this***

   $flyMean,$flySEM,$flyCall,$description)=split (/\t/,$_);

$length=length($hits{$oligo});
#print "oligo=$oligo length=$length\n";
if ($hits{$oli}) {
   $arraydata=$_;
   $arraymatch++;
#   print "Outputting for $oli",br;
   &output;
	}
}	
close INFILE;
}

sub output {
$annotstring=$hits{$oli};
 @o=split(/\t/,$annotstring);
$fbgn=$o[24];
$o[22] =~ s/([A-Z]+_[\.0-9]+)/<a href=http:\/\/www.ncbi.nlm.nih.gov\/entrez\/query.fcgi?db=Protein&cmd=search&term=$1 target=_blank>$1<\/a>;/g;
$o[23] =~ s/([A-Z]+_[\.0-9]+)/<a href=http:\/\/www.ncbi.nlm.nih.gov\/entrez\/query.fcgi?db=Nucleotide&cmd=search&term=$1 target=_blank>$1<\/a>;/g;
$o[24] =~ s/(FBgn[0-9]+)/<a href=http:\/\/flybase\.bio\.indiana\.edu\/\.bin\/fbidq\.html?$1 target=_blank>$1<\/a>/g;

	$go=$o[30];
	$go=~ s/\/\/[^\/]+\/\/\//; /g;
	$go=~ s/ inferred [^\/]+//g;
	$go=~ s/\/\//\//g;
	$go=substr($go,0,120);
	$go =~ s/([0-9]+)/<a href=http:\/\/amigo.geneontology.org\/cgi-bin\/amigo\/go.cgi?action=query&view=query&query=$1&search_constraint=terms target=_blank>$1<\/a>/g;
   $short_desc=  "$o[24]: $o[13]: $go";  
	print "<tr><td>$oli</td><td>$brainMean</td><td>$headMean</td><td>$tagMean</td><td>$sgMean</td><td>$cropMean</td><td>$midgutMean</td><td>$tubuleMean</td><td>$hindgutMean</td><td>$ovaryMean</td><td>$testisMean</td><td>$accMean</td><td>$carMean</td><td>$l_tubMean</td><td>$l_fatMean</td><td>$flyMean</td><td>$short_desc</td></tr>"; 	
	}
	