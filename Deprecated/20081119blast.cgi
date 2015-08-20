#!c:/perl/bin/perl.exe
#Atlas v 0.1
#JATD 9/4/07
#***places to add code for new tissues are marked like this***

use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
$ua = $ENV{REMOTE_ADDR};
$annot_file="Drosophila_2.na23.annot.csv";
$array_file="all.txt";
$summary_file="gene_summaries.tsv";
$maxhits=10;
$critlevel=-10;

&do_headers;
&do_form;

if (param()) {
   $search=param('name');
   print "<hr>";

if (length($search)>2) {
open(TEMPFILE,">temp.txt") || die "Cant open tempfile";
   print TEMPFILE "$search\n";
   close TEMPFILE;
	$s="";
	$t=time;
	&read_homophila;
	&read_insitu;
	&read_array;
	&read_summaries;
	&do_blast;
	$elapsed=time-$t;
}
#print "Looking for $search. $match entries matched from $n, in $elapsed s. \n",p;
}
&do_footer;


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
print	start_form,    "Paste your <b>protein</b> sequence here: ",br,textarea('name','',10,80), submit,br,
    "(Spaces, numbers, blank lines are ignored. Search takes around 10 s.)", p;
    submit,
    end_form,
    hr;
print end_html;
}

sub search_annot {
#readaffy annotation file data
open(ANNOT,"<$annot_file") || die "Cant get $annot_file file";
#read in the data file
$n=0;
$match=0;

while (<ANNOT>) {
   $n++;
   chomp();
#   $_=~s/([0-9]), ([0-9])/$1 $2/g;
   $_=~s/---//g;
#   $_=~s/,/\t/g;
#   $_=~s/\"//g;
   $_=~s/\",\"/\t/g;
$ST=uc($_);

    if ($ST=~/$s/) {
		$match++;
#		print "Match $match\n",br;
		if ($_=~/([0-9]+_[_astx]+)/ )   {
			$oligo=$1;
#			print "$oligo",br;
			$hits{$oligo}=$_;
			}
	}
	if ($match > $maxhits) {
	   print "You got more than $maxhits hits better than e$critprob. Just showing the first $maxhits\!\n";
	   last;
	   close ANNOT;
	   }
	if ($ST =~ /AFFYMETRIX/) {
	   last;
	   close ANNOT;
	   }

}
close ANNOT;
print "Searching for $s through $n array annotations produced $match hits",p;
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

sub output {
 foreach $key (keys (%hits)) {
  if (length($hits{$key})>10) {
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
#***places to add code for new tissues are marked like this***
   $flyMean,$flySEM,$flyCall)=split (/\t/,$arraydata);

#print "$oli:\n",br;
$annotstring=$hits{$key};
 @o=split(/\t/,$annotstring);
#print "Oligo:$oli, annot: $annotstring",p;
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
         
      print "<font size=\"-1\" face=\"Verdana, Arial, Helvetica, sans-serif\"><table border=2><tr><td>Tissue</td><td>mRNA Signal</td><td>Present Call</td><td>Enrichment</td><td>Affy Call</td><td bgcolor=#CCCCCC width=\"30%\">Flybase summary</td></tr>";
      printf ("<tr><td>Brain</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$brain_fly_t</td><td rowspan=14 bgcolor=#CCCCCC>$summary{$fbgn}</td></tr>",$brainMean,$brainSEM,$brainCall,$brainRatio);
      printf ("<tr><td>Head</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$head_fly_t</td></tr>",$headMean,$headSEM,$headCall,$headRatio);
      printf ("<tr><td>Thoracicoabdominal ganglion</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$tag_fly_t</td></tr>",$sgMean,$sgSEM,$sgCall,$sgRatio);
      printf ("<tr><td>Salivary gland</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$sg_fly_t</td></tr>",$tagMean,$tagSEM,$tagCall,$tagRatio);
      printf ("<tr><td>Crop</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$crop_fly_t</td></tr>",$cropMean,$cropSEM,$cropCall,$cropRatio);
      printf ("<tr><td>Midgut</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$midgut_fly_t</td></tr>",$midgutMean,$midgutSEM,$midgutCall,$midgutRatio);
      printf ("<tr><td>Tubule</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$tubule_fly_t</td></tr>",$tubuleMean,$tubuleSEM,$tubuleCall,$tubuleRatio);
      printf ("<tr><td>Hindgut</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$hindgut_fly_t</td></tr>",$hindgutMean,$hindgutSEM,$hindgutCall,$hindgutRatio);
      printf ("<tr><td>Ovary</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$ovary_fly_t</td></tr>",$ovaryMean,$ovarySEM,$ovaryCall,$ovaryRatio);
      printf ("<tr><td>Testis</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$testis_fly_t</td></tr>",$testisMean,$testisSEM,$testisCall,$testisRatio);
      printf ("<tr><td>Male accessory glands</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$acc_fly_t</td></tr>",$accMean,$accSEM,$accCall,$accRatio);
      printf ("<tr><td>Adult carcass</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$car_fly_t</td></tr>",$carMean,$carSEM,$carCall,$carRatio);
      printf ("<tr><td>Larval tubule</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$l_tub_fly_t</td></tr>",$l_tubMean,$l_tubSEM,$l_tubCall,$l_tubRatio);
      printf ("<tr><td>Larval fat body</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$l_fat_fly_t</td></tr>",$l_fatMean,$l_fatSEM,$l_fatCall,$l_fatRatio);
#***places to add code for new tissues are marked like this***

      printf ("<tr><td>Whole fly</td><td>%d \xb1 %d</td><td>%d of 4</td><td> </td><td> </td></tr>",$flyMean,$flySEM,$flyCall);
      print "</font></table>",p;
	  $hits{$key}="";
 	}
	}
}

sub read_insitu {
#read in BDGP in situ data
open(INSITU,"insitu.txt") || die "Cant get insitu.txt file";
while (<INSITU>) {
   chop;
   ($gen,$cg,$FBgn,$emb_pix,$emb_tissues)=split (/\t/,$_);
   $ep{$FBgn}=$emb_pix;
   $et{$FBgn}=$emb_tissues;
   $es{$FBgn}=$gen;
   }
close INSITU;
}

sub read_homophila {
#read in homophila data
open(HOMOPHILA,"homophila.txt") || die "Cant get homophila.txt file";
while (<HOMOPHILA>) {
   chop;
   ($cg,$omim,$refseq,$evalue,$gen,$descript,$disease)=split (/\t/,$_);
   $cg=~ s/-P[A-Z]//;
   $ev{$cg}=$evalue;
   $om{$cg}=$omim;
   $re{$cg}=$refseq;
   $ge{$cg}=$gen;
   $di{$cg}=$disease;
   }
close HOMOPHILA;
}
sub do_blast {
#constants
$window=20;
$crit_score=3;
$file=$ARGV[0];
$files=0;
$starttime=time;
$seq="";
$id="";
$l=0;
#print output spreadsheet headings

$out="temp.blastp";
#fly
system("c:\\blast\\blastall.exe -p blastp -d c:\\blast\\data\\dmelpep.fasta -i \"c:\\Program files\\Apache\\htdocs\\atlas\\temp.txt\" -o $out");
   # if ($? == -1) {
	# print "failed to execute: $!\n";
    # }
    # elsif ($? & 127) {
	# printf "child died with signal %d, %s coredump\n",
	    # ($? & 127),  ($? & 128) ? 'with' : 'without';
    # }
    # else {
	# printf "child exited with value %d\n", $? >> 8;
    # }
&parse;
}

sub parse {
  open(BLASTFILE,"<$out") || die "Cant get $out file";
   $found=0;
   while (<BLASTFILE>) {
      chomp ();
#	  print "$_",br;
         if (($_ =~ /e(-[0-9]+)/) || ($_ =~/(0\.0)/)) {
             $prob=$1;
#              print  "Sig match : $_\n",br;
			 $fullprob="e$1";
              if (($prob<$critlevel) || ($prob == 0)) {
                 $found++;
                $gene="";
                $genus=""; 
                $ann="";

#look for fly genes
                if ($_ =~ /(CG[0-9]+)/) {
				$gene=$1;
				$ann="";
				$ann=$dmeldesc{$gene};
				 $bestdmelprob=$fullprob;
                 $bestdmelgene=$gene;
                 $bestdmeldesc=$ann;
#				 print STDERR "$gene: $fullprob: $ann\n",br;
				print hr,"BLASTP hit for Drosophila gene $gene, with probability $bestdmelprob",p;
				$s="$gene-";
				&search_annot;
				&output;
                 if ($found>$maxhits) {
				    print "More than $maxhits close matches found. Just showing you the first $maxhits",p;
					close BLASTFILE;
					}
                }

             }
       }

}
close BLASTFILE;
}

sub read_annot {
     $org="dmel";
	$keyfilename="$org"."_key.txt";
    open(KEYFILE,"<$keyfilename") || die "Cant get $keyfilename file";
    while (<KEYFILE>) {
	    chomp();
	    ($num,$b,$c)=split(/\t/);
		$_ =~ s/\t/; /g;
	    $dmeldesc{$num}.=", $_";
        }
    close KEYFILE;
}

sub read_summaries {
#read in flybase summary data
open(SUMMARYFILE,$summary_file) || die "Cant get $summary_file file";
while (<SUMMARYFILE>) {
   chomp;
   ($fb,$de)=split(/\t/);
   $summary{$fb}=$_;
   }
close SUMMARYFILE;
}

sub do_footer {
print hr,"<P align=CENTER><font SIZE=1>Chintapalli, V. R., Wang, J. and Dow, J. A. T. (2007). Using FlyAtlas to identify better Drosophila models of human disease. <a href=http://www.nature.com/ng/journal/v39/n6/abs/ng2049.html target=_blank><i>Nature Genetics</i> 39: 715-720</a></font></P>";

print end_html;
}