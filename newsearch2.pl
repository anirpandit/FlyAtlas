#!c:/perl/bin/perl.exe
#Atlas v 0.1
#JATD 9/4/07
#***places to add code for new tissues are marked like this***

use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
$ua = $ENV{REMOTE_ADDR};
	$annot_file="Drosophila_2.na22.annot.csv";
	$array_file="all.txt";

&do_headers;

&do_form;

if (param()) {
   $search=param('name');
   print "<hr>";

if (length($search)>2) {
	$s=uc($search);
	&read_homophila;
	&read_insitu;
	$t=time;
	&search_annot;
	&pull_data;

	$elapsed=time-$t;

}
print "Looking for $search. $match entries matched from $n, in $elapsed s. Read $m lines from array file, and matched $arraymatch.\n",p;
}

sub do_headers {
print header;
print start_html('The Drosophila adult expression atlas');
print "<font  size=-1 face=\"Verdana, Arial, Helvetica, sans-serif\">";
print "<table border=0 width=\"100%\"><tr><td><a href=http://www.gla.ac.uk><img src=crest.gif align=LEFT alt=\"University of Glasgow\" Width=200></a></td>";
print  "<td><h1>Search the Drosophila adult expression atlas</h1></td>";
print "<td><a href=http://www.bbsrc.ac.uk><img src=bbsrcsmallcolour.gif align=RIGHT width=200 alt=\"Biotechnology & Biological Sciences Research Council\"></a></td></tr></table>";

print "<table width=\"100%\" border=\"1\" cellpadding=\"2\"><tr> ";
print "<td><div align=\"center\"><font color=\"#0033FF\" size=\"1\"><a href=\"atlas.cgi\">Home   &amp; Search</a></font></div></td>";
print "<td><div align=\"center\"><font color=\"#0033FF\" size=\"1\"><a href=\"batch_table.cgi\">Batch/table Search</a></font></div></td>";
print "<td><div align=\"center\"><font color=\"#0033FF\" size=\"1\"><a href=\"tissues.cgi\">Tissues Search</a></font></div></td>";
print " <td><div align=\"center\"><font color=\"#0033FF\" size=\"1\"><a href=\"about_atlas.html\">About & FAQ</a></font></div></td>";
print " <td><div align=\"center\"><font color=\"#0033FF\" size=\"1\"><a href=\"top50.html\">Top 50</a></font></div></td>";
print " <td><div align=\"center\"><font color=\"#0033FF\" size=\"1\"><a href=\"data.html\">Original data</a></font></div></td>";
print " <td><div align=\"center\"><font color=\"#0033FF\" size=\"1\"><a href=\"links.html\">Links</a></font></div></td></tr></table>";

#***places to add code for new tissues are marked like this***
open(INFILE,"news.txt") || die "Cant get newsfile";
while (<INFILE>) {
   chop;
   print "<b>Latest news: $_</b>",br;
   }
close INFILE;   
print p,"This dataset was generated by Venkat Chintapalli, Jing Wang & <a href=http://www.gla.ac.uk:443/ibls/staff/staff.php?who=PedeSP>Julian Dow</a> at the University of Glasgow with funding from the UK's BBSRC.",br;
print "It is intended to give you a quick answer to the question: <i>where is my gene of interest expressed/enriched in the adult fly?</i> ";
print "For each gene & tissue, you're given the mRNA SIGNAL (how abundant the mRNA is), the mRNA ENRICHMENT (compared to whole flies), and the Affymetrix PRESENT CALL (out of 4 arrays, how many times it was detectably expressed).",br;
print "New! You can also <a href=tissues.cgi>order your results by tissue, and by enrichment.</a><br>";
}

sub do_form {
print	start_form,    "String to look for? ",textfield('name'),
    "e.g. vha, cell adhesion, receptor, aquaporin, adenylate, CG1147, pnt", p,
" If you don\'t get a hit for a particular gene, look it up ",
" in Flybase and try any synonyms (FBgn number, CG number, etc)",p;
    submit,
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

while (<INFILE>) {
   $n++;
   chomp();
#   $_=~s/([0-9]), ([0-9])/$1 $2/g;
   $_=~s/---//g;
#   $_=~s/,/\t/g;
#   $_=~s/\"//g;
   $_=~s/\",\"/\t/g;
$ST=uc($_);

    if ($ST=~$s) {
		$match++;
		if ($_=~/([0-9]+_[_astx]+)/ )   {
			$oligo=$1;
#			print "$oligo",br;
			$hits{$oligo}=$_;
			}
	}
	if ($match > 500) {
	   print "You got more than 500 hits. Just showing the first 500.\n";
	   last;
	   close INFILE;
	   }
	if ($ST =~ /AFFYMETRIX/) {
	   last;
	   close INFILE;
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
#***places to add code for new tissues are marked like this***

   $flyMean,$flySEM,$flyCall,$description)=split (/\t/,$_);

$length=length($hits{$oligo});
#print "oligo=$oligo length=$length\n";
if ($hits{$oli}) {
   $arraydata=$_;
   $arraymatch++;
   &output;
	}
}	
close INFILE;
}

sub output {
$annotstring=$hits{$oli};
 @o=split(/\t/,$annotstring);
# print "$annotstring",p;
$fbgn=$o[24];
$o[22] =~ s/([A-Z]+_[\.0-9]+)/<a href=http:\/\/www.ncbi.nlm.nih.gov\/entrez\/query.fcgi?db=Protein&cmd=search&term=$1 target=_blank>$1<\/a>;/g;
$o[23] =~ s/([A-Z]+_[\.0-9]+)/<a href=http:\/\/www.ncbi.nlm.nih.gov\/entrez\/query.fcgi?db=Nucleotide&cmd=search&term=$1 target=_blank>$1<\/a>;/g;
$o[24] =~ s/(FBgn[0-9]+)/<a href=http:\/\/flybase\.bio\.indiana\.edu\/\.bin\/fbidq\.html?$1 target=_blank>$1<\/a>/g;

 	print "<b>$o[13] ($o[14])  $o[17]; $o[24]; <a href=http://flyatlas.org/probeset.cgi?name=$oli target=_blank>$oli</a></b>\n",br; 
 	print "Accessions: $o[22] $o[23]\n",br; 
	$go=$o[30];
	$go=~ s/\/\/[^\/]+\/\/\//; /g;
	$go=~ s/ inferred [^\/]+//g;
	$go=~ s/\/\//\//g;
	$go=substr($go,0,120);
	$go =~ s/([0-9]+)/<a href=http:\/\/amigo.geneontology.org\/cgi-bin\/amigo\/go.cgi?action=query&view=query&query=$1&search_constraint=terms target=_blank>$1<\/a>/g;
	$pa=substr($o[33],0,120);
	$ip=substr($o[34],0,120);
 	print "GeneOntology: $go\n",br; 
 	print "Pathway: $pa\n",br; 
 	print "Interpro: $ip\n",br; 
#look for matching BDGP in situ data
      $symbol="";
      if ($es{$fbgn}) {
         $symbol=$es{$fbgn};
         print "<a href=http://www.fruitfly.org/cgi-bin/ex/insitu.pl target=_blank>BDGP gene expression</a> has <a href=http://www.fruitfly.org/cgi-bin/ex/bquery.pl?qtype=report&qpage=queryresults&searchfield=symbol&find=$symbol target=_blank>embryonic in situ data for $symbol</a>: $ep{$fbgn} pix of staining in $et{$fbgn} body parts.",br;
         }

#look for matching homophila data 
        $omim="";
#       print "$cg",br;
        $cg=$o[17];
		$omim=$om{$cg};
      if ($omim) {
         print "<a href=http://superfly.ucsd.edu/homophila/ target=_blank>Homophila</a> reports that $cg is a close match ($ev{$cg}) to  human gene $ge{$cg} (<a href=http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?db=gene&cmd=search&term=$re{$cg} target=_blank>$re{$cg}</a>), a gene associated with <a href=http://www.ncbi.nlm.nih.gov/entrez/dispomim.cgi?id=$om{$cg} target=_blank>$di{$cg}</a>.",br;
         }
         
      print "<font size=\"-1\" face=\"Verdana, Arial, Helvetica, sans-serif\"><table border=2><tr><td>Tissue</td><td>mRNA Signal</td><td>Present Call</td><td>Enrichment</td><td>Affy Call</td></tr>";
      printf ("<tr><td>Brain</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$brain_fly_t</td></tr>",$brainMean,$brainSEM,$brainCall,$brainRatio);
      printf ("<tr><td>Head</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$head_fly_t</td></tr>",$headMean,$headSEM,$headCall,$headRatio);
      printf ("<tr><td>Crop</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$crop_fly_t</td></tr>",$cropMean,$cropSEM,$cropCall,$cropRatio);
      printf ("<tr><td>Midgut</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$midgut_fly_t</td></tr>",$midgutMean,$midgutSEM,$midgutCall,$midgutRatio);
      printf ("<tr><td>Tubule</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$tubule_fly_t</td></tr>",$tubuleMean,$tubuleSEM,$tubuleCall,$tubuleRatio);
      printf ("<tr><td>Hindgut</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$hindgut_fly_t</td></tr>",$hindgutMean,$hindgutSEM,$hindgutCall,$hindgutRatio);
      printf ("<tr><td>Ovary</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$ovary_fly_t</td></tr>",$ovaryMean,$ovarySEM,$ovaryCall,$ovaryRatio);
      printf ("<tr><td>Testis</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$testis_fly_t</td></tr>",$testisMean,$testisSEM,$testisCall,$testisRatio);
      printf ("<tr><td>Male accessory glands</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$acc_fly_t</td></tr>",$accMean,$accSEM,$accCall,$accRatio);
      printf ("<tr><td>Larval tubule</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$l_tub_fly_t</td></tr>",$l_tubMean,$l_tubSEM,$l_tubCall,$l_tubRatio);
      printf ("<tr><td>Larval fat body</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$l_fat_fly_t</td></tr>",$l_fatMean,$l_fatSEM,$l_fatCall,$l_fatRatio);
#***places to add code for new tissues are marked like this***

      printf ("<tr><td>Whole fly</td><td>%d \xb1 %d</td><td>%d of 4</td><td> </td><td> </td></tr>",$flyMean,$flySEM,$flyCall);
      print "</font></table>",p;
 	}



sub read_insitu {
#read in BDGP in situ data
open(INFILE,"insitu.txt") || die "Cant get insitu.txt file";
while (<INFILE>) {
   chop;
   ($gen,$cg,$FBgn,$emb_pix,$emb_tissues)=split (/\t/,$_);
   $ep{$FBgn}=$emb_pix;
   $et{$FBgn}=$emb_tissues;
   $es{$FBgn}=$gen;
   }
close INFILE;
}

sub read_homophila {
#read in homophila data
open(INFILE,"homophila.txt") || die "Cant get homophila.txt file";
while (<INFILE>) {
   chop;
   ($cg,$omim,$refseq,$evalue,$gen,$descript,$disease)=split (/\t/,$_);
   $cg=~ s/-P[A-Z]//;
   $ev{$cg}=$evalue;
   $om{$cg}=$omim;
   $re{$cg}=$refseq;
   $ge{$cg}=$gen;
   $di{$cg}=$disease;
   }
close INFILE;
}