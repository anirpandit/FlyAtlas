#!/usr/bin/perl
#batch table
#ver 1.1
#JATD 19/09/09
#***places to add code for new tissues are marked like this***

use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
$ua = $ENV{REMOTE_ADDR};
$annot_file="Drosophila_2.na32.annot.csv";
$array_file="20090519all.txt";
$biogrid_file="BIOGRID-ORGANISM-Drosophila_melanogaster-2.0.52.tab.txt";
$homophila_file="homophila_10.txt";
$wien_file="REPORT_VdrcCatalogue.txt";
$maxhits=200;

&do_headers;

&do_form;
if (param()) {
#   &read_homophila;
#	&read_insitu;
	$t=time;
print "<font size=-1><table border=2 style=\"font-size: 11px\">";
#***places to add code for new tissues are marked like this***
print "<tr><td>oligo</td><td>brainMean</td><td>headMean</td><td>eyeMean</td><td>tagMean</td><td>sgMean</td><td>cropMean</td><td>midgutMean</td><td>tubuleMean</td><td>hindgutMean</td><td>heartMean</td><td>fatbodyMean</td><td>ovaryMean</td><td>testisMean</td><td>accMean</td><td>v_sptMean</td><td>m_sptMean</td><td>carMean</td><td>l_CNSMean</td><td>l_sgMean</td><td>l_midgutMean</td><td>l_tubuleMean</td><td>l_hindgutMean</td><td>l_fatMean</td><td>l_traMean</td><td>l_carMean</td><td>lS2Mean</td><td>flyMean</td><td>description</td></tr>";
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
  &read_array;
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

sub read_array {
#read aa data
open(ARRAY,"<$array_file") || die "Cant get $array_file file";
$ar=0;
#read in the data file
while (<ARRAY>) {
   chomp();
   $ar++;
		if ($_=~/([0-9]+_[_astx]+)/ )   {
			$oligo=$1;
      $array{$oligo}=$_;
	}	
}
	close ARRAY;
#print "Read in $ar lines of array data.",br;
}

sub pull_data {
foreach $key (keys (%hits)) {
 #get the array data and assign to variables
	$arraydata=$array{$key};  
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
   $l_sg_fly_t,$l_sgMean,$l_sgSEM,$l_sgCall,$l_sgRatio,
   $l_midgut_fly_t,$l_midgutMean,$l_midgutSEM,$l_midgutCall,$l_midgutRatio,
   $l_hindgut_fly_t,$l_hindgutMean,$l_hindgutSEM,$l_hindgutCall,$l_hindgutRatio,
   $v_spt_fly_t,$v_sptMean,$v_sptSEM,$v_sptCall,$v_sptRatio,
   $m_spt_fly_t,$m_sptMean,$m_sptSEM,$m_sptCall,$m_sptRatio,
   $l_cns_fly_t,$l_cnsMean,$l_cnsSEM,$l_cnsCall,$l_cnsRatio,
   $a_fat_fly_t,$a_fatMean,$a_fatSEM,$a_fatCall,$a_fatRatio,
   $l_car_fly_t,$l_carMean,$l_carSEM,$l_carCall,$l_carRatio,
   $a_eye_fly_t,$a_eyeMean,$a_eyeSEM,$a_eyeCall,$a_eyeRatio,
   $a_hrt_fly_t,$a_hrtMean,$a_hrtSEM,$a_hrtCall,$a_hrtRatio,
   $l_tra_fly_t,$l_traMean,$l_traSEM,$l_traCall,$l_traRatio,
   $S2_fly_t,$S2Mean,$S2SEM,$S2Call,$S2Ratio,
#***places to add code for new tissues are marked like this***
   $flyMean,$flySEM,$flyCall)=split (/\t/,$arraydata);

#print "$oli:l_cns_fly_t: $l_cns_fly_t\n",br;
$annotstring=$hits{$key};
 @o=split(/\t/,$annotstring);
#print "Oligo:$oli, annot: $annotstring",p;
$fbgn=$o[24];
$o[22] =~ s/([A-Z]+_[\.0-9]+)/<a href=http:\/\/www.ncbi.nlm.nih.gov\/entrez\/query.fcgi?db=Protein&cmd=search&term=$1 target=_blank>$1<\/a>;/g;
$o[23] =~ s/([A-Z]+_[\.0-9]+)/<a href=http:\/\/www.ncbi.nlm.nih.gov\/entrez\/query.fcgi?db=Nucleotide&cmd=search&term=$1 target=_blank>$1<\/a>;/g;
$o[24] =~ s/(FBgn[0-9]+)/<a href=http:\/\/flybase\.bio\.indiana\.edu\/\.bin\/fbidq\.html?$1 target=_blank>$1<\/a>/g;

# 	print "<b>$o[13] ($o[14])  $o[17]; $o[24]; <a href=http://flyatlas.org/probeset.cgi?name=$oli target=_blank>$oli</a></b>\n",br; 
# 	print "Accessions: $o[22] $o[23]\n",br; 
	$go=$o[30];
	$go=~ s/\/\/[^\/]+\/\/\//; /g;
	$go=~ s/ inferred [^\/]+//g;
	$go=~ s/\/\//\//g;
	$go=substr($go,0,120);
	$go =~ s/([0-9]+)/<a href=http:\/\/amigo.geneontology.org\/cgi-bin\/amigo\/go.cgi?action=query&view=query&query=$1&search_constraint=terms target=_blank>$1<\/a>/g;
	$pa=substr($o[33],0,120);
	$ip=substr($o[34],0,120);
	$cg=$o[8];
	$cg =~ s/\-R[A-Z]//;
   $short_desc=  "$o[24]: $o[13]: $go";  
	print "<tr><td>$oli</td><td>$brainMean</td><td>$headMean</td><td>$a_eyeMean</td><td>$tagMean</td><td>$sgMean</td><td>$cropMean</td><td>$midgutMean</td><td>$tubuleMean</td><td>$hindgutMean</td><td>$a_hrtMean</td><td>$a_fatMean</td><td>$ovaryMean</td><td>$testisMean</td><td>$accMean</td><td>$v_sptMean</td><td>$m_sptMean</td><td>$carMean</td><td>$l_cnsMean</td><td>$l_sgMean</td><td>$l_midgutMean</td><td>$l_tubMean</td><td>$l_hindgutMean</td><td>$l_fatMean</td><td>$l_traMean</td><td>$l_carMean</td><td>$S2Mean</td><td>$flyMean</td><td>$short_desc</td></tr>"; 	
	}
	}