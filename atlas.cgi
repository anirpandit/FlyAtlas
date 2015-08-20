#!/usr/bin/perl
#Atlas v 0.1
#JATD 9/4/07
#***places to add code for new tissues are marked like this***

use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
$ua = $ENV{REMOTE_ADDR};

#Need to store as database table##

$annot_file="Drosophila_2.na32.annot.csv"; 
$array_file="all.txt";
$biogrid_file="BIOGRID-ORGANISM-Drosophila_melanogaster-2.0.52.tab.txt";
$homophila_file="homophila_10.txt";
$wien_file="REPORT_VdrcCatalogue.txt";
$trip_file="trip.txt";
$maxhits=400;

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
	  &read_trip;
	  &search_annot;
	  &output;
	  $elapsed=time-$t;
   }

   print "Looking for $search. $match entries matched from $n, in $elapsed s. \n",p;
}

sub read_homophila {
   #read in homophila data
   open(HOMOPHILA,$homophila_file) || die "Cant get $homophila_file file";
   while (<HOMOPHILA>) {
      chomp;
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

sub read_biogrid {
   #read in biogrid data
   open(BIOGRID,$biogrid_file) || die "Cant get $biogrid_file file";
   while (<BIOGRID>) {
      chomp;
      @bg=split (/\t/,$_); 
      if ($bg[0] =~/(CG[0-9]+)/) {
         $target=$bg[1];
         $bgarr{$1}.="<a href=http://flybase.bio.indiana.edu/.bin/fbidq.html?$target target=_blank>$target</a> ";
      }
   }
   close BIOGRID;
}

sub read_insitu {
   #read in BDGP in situ data
   open(INSITU,"insitu.txt") || die "Cant get insitu.txt file";
   while (<INSITU>) {
      chomp;
      ($gen,$cg,$FBgn,$emb_pix,$emb_tissues)=split (/\t/,$_);
      $ep{$FBgn}=$emb_pix;
      $et{$FBgn}=$emb_tissues;
      $es{$FBgn}=$gen;
      }
   close INSITU;
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

sub read_wien {
#read in Vienna RNAi data
open(WIEN,$wien_file) || die "Cant get wien.txt file";
while (<WIEN>) {
   chomp;
if ($_=~/(FBgn[0-9]+)/) {
   @v=split(/\t/,$_);
   $wien{$1}++;
   $wienstat{$1}.="$v[8],";
   }
}
close WIEN;
}

sub read_trip {
#read in Harvard TrIP RNAi data
open(TRIP,$trip_file) || die "Cant get wien.txt file";
while (<TRIP>) {
   chomp;
if ($_=~/(FBgn[0-9]+)/) {
   $trip{$1}++;
   }
}
close TRIP;
}

sub search_annot {
   #readaffy annotation file data
   open(ANNOT,"<$annot_file") || die "Cant get $annot_file file";
   #read in the data file
   $n=0;
   $match=0;

   while (<ANNOT>) 
   {
      $n++;
      if ($_ =~/[0-9]+_[_astx]+/) 
      {
         chomp();
         #$_=~s/([0-9]), ([0-9])/$1 $2/g;
         $_=~s/---//g;
         #$_=~s/,/\t/g;
         #$_=~s/\"//g;
         $_=~s/\",\"/\t/g;
         $ST=uc($_);

         if ($ST=~/$s/) 
         {
            $match++;
            #print "Match $match\n",br;
            if ($_=~/([0-9]+_[_astx]+)/ )   
            {
               $oligo=$1; 
               #print "$oligo",br;
               $hits{$oligo}=$_;
            }
         }
         
         if ($match > $maxhits) 
         {
            print "You got more than $maxhits hits. Just showing the first $maxhits.\n";
            last;
            close ANNOT;
         }
   
         if ($ST =~ /AFFYMETRIX/) 
         {
            last;
            close ANNOT;
         }
      }
   }
   close ANNOT;
   print "Searching for $s through $n annotations produced $match hits",p;
}  


sub output 
{
   foreach $key (keys (%hits)) 
   {
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
      # print  "$annotstring",br;
      @o=split(/,/,$annotstring);
      #print "Oligo:$oli, annot: $annotstring",p;
      #for ($i=0;$i<30; $i++) {
      #   print "$i: $o[$i]",br;
      #   }

      $fbgn=$o[19];
      $o[24] =~ s/([A-Z]+_[\.0-9]+)/<a href=http:\/\/www.ncbi.nlm.nih.gov\/entrez\/query.fcgi?db=Protein&cmd=search&term=$1 target=_blank>$1<\/a>;/g;
      $o[25] =~ s/([A-Z]+_[\.0-9]+)/<a href=http:\/\/www.ncbi.nlm.nih.gov\/entrez\/query.fcgi?db=Nucleotide&cmd=search&term=$1 target=_blank>$1<\/a>;/g;
      $o[26] =~ s/(FBgn[0-9]+)/<a href=http:\/\/flybase\.bio\.indiana\.edu\/\.bin\/fbidq\.html?$1 target=_blank>$1<\/a>/g;
      $cg=$o[7];
      $cg =~ s/\-R[A-Z]//;

      print "<b>$o[15] ($o[16])</b>; $cg; $o[19] @ <a href=http://flybase.org/cgi-bin/gbrowse2/dmel/?name=$fbgn target=_blank>$o[14]</a>; probeset <a href=http://flyatlas.org/probeset.cgi?name=$oli target=_blank>$oli</a>\n",br; 
      print "<SMALL>Accessions: protein= $o[24], nucleotide= $o[25]\n",br; 
      $go=$o[30];
      $go=~ s/\/\/[^\/]+\/\/\//; /g;
      $go=~ s/ inferred [^\/]+//g;
      $go=~ s/\/\//\//g;
      $go=substr($go,0,120);
      $go =~ s/([0-9]+)/<a href=http:\/\/amigo.geneontology.org\/cgi-bin\/amigo\/go.cgi?action=query&view=query&query=$1&search_constraint=terms target=_blank>$1<\/a>/g;
      $pa=substr($o[33],0,120);
      $ip=substr($o[34],0,120);

   
      if ($go) 
      {
         print "GeneOntology: $go\n",br; 
      }
      if ($pa) 
      {
         print "Pathway: $pa\n",br; 
      }
      if ($ip) 
      {  
         print "Interpro: $ip\n",br; 
      }
      
      #look for Flymine data
      if ($fbgn) 
      { 
         print "<a href=http://www.flymine.org/query/portal.do?origin=flybase&class=gene&externalid=$fbgn target=_blank>FlyMine data</a> for $fbgn.",br;
      }
      
      #look for matching BDGP in situ data
      $symbol="";
      if ($es{$fbgn}) 
      {
         $symbol=$es{$fbgn};
         print "<a href=http://www.fruitfly.org/cgi-bin/ex/insitu.pl target=_blank>BDGP gene expression</a> has <a href=http://www.fruitfly.org/cgi-bin/ex/bquery.pl?qtype=report&qpage=queryresults&searchfield=symbol&find=$symbol target=_blank>embryonic in situ data for $symbol</a>: $ep{$fbgn} pix of staining in $et{$fbgn} body parts.",br;
      }

      #look for matching homophila data 
      $omim="";
      #print "CG= $cg",br;
      $omim=$om{$cg};
      if ($omim) 
      {
            print "<a href=http://superfly.ucsd.edu/homophila/ target=_blank>Homophila</a> reports that $cg is a close match ($ev{$cg}) to  human gene $ge{$cg} (<a href=http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?db=gene&cmd=search&term=$re{$cg} target=_blank>$re{$cg}</a>), a gene associated with <a href=http://www.ncbi.nlm.nih.gov/entrez/dispomim.cgi?id=$om{$cg} target=_blank>$di{$cg}</a>.",br;
      }
 
      #look for matching biogrid data 
      $bgstring="";
      #print "$cg",br;
      $bgstring=$bgarr{$cg};
      if ($bgstring) 
      {
         print "<a href=http://www.thebiogrid.org/index.php target=_blank>BioGrid</a> reports that $cg interacts with $bgstring.",br;
      }
 
      #look for matching Vienna data 
      if ($trip{$fbgn}) 
      {
         print "<a href=http://www.flyrnai.org/TRiP-HOME.html target=_blank>TRiP</a> has $trip{$fbgn} RNAi stocks for $fbgn</a> available for purchase.",br;
      }
  
      #look for matching Trip data 
      if ($wien{$fbgn}) 
      {
         print "<a href=http://stockcenter.vdrc.at/control/main target=_blank>VDRC</a> has $wien{$fbgn} <a href=http://stockcenter.vdrc.at/control/checkAdvancedSearch?VIEW_SIZE=100&SEARCH_CATEGORY_ID=VDRC_All&fb_number=$fbgn target=_blank>RNAi stocks for $fbgn</a> available for purchase.",br;
      }
         
      printf "<font face=\"Verdana, Arial, Helvetica, sans-serif\"><table border=2 style=\"font-size: 11px\"><tr><td>Tissue</td><td>mRNA Signal</td><td>Present Call</td><td>Enrichment</td><td>Affy Call</td></tr>";
      printf ("<tr><td>Brain</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$brain_fly_t</td></tr>",$brainMean,$brainSEM,$brainCall,$brainRatio);
      printf ("<tr><td>Head</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$head_fly_t</td></tr>",$headMean,$headSEM,$headCall,$headRatio);
      printf ("<tr><td>Eye</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$a_eye_fly_t</td></tr>",$a_eyeMean,$a_eyeSEM,$a_eyeCall,$a_eyeRatio);
      printf ("<tr><td>Thoracicoabdominal ganglion</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$tag_fly_t</td></tr>",$tagMean,$tagSEM,$tagCall,$tagRatio);
      printf ("<tr><td>Salivary gland</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$sg_fly_t</td></tr>",$sgMean,$sgSEM,$sgCall,$sgRatio);
      printf ("<tr><td>Crop</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$crop_fly_t</td></tr>",$cropMean,$cropSEM,$cropCall,$cropRatio);
      printf ("<tr><td>Midgut</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$midgut_fly_t</td></tr>",$midgutMean,$midgutSEM,$midgutCall,$midgutRatio);
      printf ("<tr><td>Tubule</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$tubule_fly_t</td></tr>",$tubuleMean,$tubuleSEM,$tubuleCall,$tubuleRatio);
      printf ("<tr><td>Hindgut</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$hindgut_fly_t</td></tr>",$hindgutMean,$hindgutSEM,$hindgutCall,$hindgutRatio);
      printf ("<tr><td>Heart</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$a_hrt_fly_t</td></tr>",$a_hrtMean,$a_hrtSEM,$a_hrtCall,$a_hrtRatio);
      printf ("<tr><td>Fat body</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$a_fat_fly_t</td></tr>",$a_fatMean,$a_fatSEM,$a_fatCall,$a_fatRatio);
      printf ("<tr><td>Ovary</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$ovary_fly_t</td></tr>",$ovaryMean,$ovarySEM,$ovaryCall,$ovaryRatio);
      printf ("<tr><td>Testis</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$testis_fly_t</td></tr>",$testisMean,$testisSEM,$testisCall,$testisRatio);
      printf ("<tr><td>Male accessory glands</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$acc_fly_t</td></tr>",$accMean,$accSEM,$accCall,$accRatio);
      printf ("<tr><td>Virgin spermatheca</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$v_spt_fly_t</td></tr>",$v_sptMean,$v_sptSEM,$v_sptCall,$v_sptRatio);
      printf ("<tr><td>Mated spermatheca</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$m_spt_fly_t</td></tr>",$m_sptMean,$m_sptSEM,$m_sptCall,$m_sptRatio);
      printf ("<tr><td>Adult carcass</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$car_fly_t</td></tr>",$carMean,$carSEM,$carCall,$carRatio);
      printf ("<tr><td>Larval CNS</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$l_cns_fly_t</td></tr>",$l_cnsMean,$l_cnsSEM,$l_cnsCall,$l_cnsRatio);
      printf ("<tr><td>Larval Salivary gland</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$l_sg_fly_t</td></tr>",$l_sgMean,$l_sgSEM,$l_sgCall,$l_sgRatio);
      printf ("<tr><td>Larval midgut</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$l_midgut_fly_t</td></tr>",$l_midgutMean,$l_midgutSEM,$l_midgutCall,$l_midgutRatio);
      printf ("<tr><td>Larval tubule</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$l_tub_fly_t</td></tr>",$l_tubMean,$l_tubSEM,$l_tubCall,$l_tubRatio);
      printf ("<tr><td>Larval hindgut</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$l_hindgut_fly_t</td></tr>",$l_hindgutMean,$l_hindgutSEM,$l_hindgutCall,$l_hindgutRatio);
      printf ("<tr><td>Larval fat body</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$l_fat_fly_t</td></tr>",$l_fatMean,$l_fatSEM,$l_fatCall,$l_fatRatio);
      printf ("<tr><td>Larval trachea</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$l_tra_fly_t</td></tr>",$l_traMean,$l_traSEM,$l_traCall,$l_traRatio);
      printf ("<tr><td>Larval carcass</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$l_car_fly_t</td></tr>",$l_carMean,$l_carSEM,$l_carCall,$l_carRatio);
      printf ("<tr><td>S2 cells (growing)</td><td>%d \xb1 %d</td><td>%d of 4</td><td>%5.2f</td><td>$S2_fly_t</td></tr>",$S2Mean,$S2SEM,$S2Call,$S2Ratio);
      #***places to add code for new tissues are marked like this***
      printf ("<tr><td>Whole fly</td><td>%d \xb1 %d</td><td>%d of 4</td><td> </td><td> </td></tr>",$flyMean,$flySEM,$flyCall);
      print "</font></table></SMALL>",p;
   }
}

sub do_headers 
{
   print "content-type: text/html \n\n"; #The header

   $HTML = "heading.html";
   open (HTML) or die "Can't open the file!";
   print <HTML>;
   close (HTML);
  
   #***places to add code for new tissues are marked like this***
   open(INFILE,"news.txt") || die "Cant get newsfile";
   while (<INFILE>) 
   {
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
   print	start_form,    
   "String to look for? ",textfield('name'), " e.g. vha, cell adhesion, receptor, aquaporin, adenylate, CG1147, pnt", p,
   submit,
   end_form,
   hr;
   print end_html;
}

&do_footer;

sub do_footer {
   print hr;
   print "<P align=CENTER><font SIZE=2>Chintapalli, V. R., Wang, J. and Dow, J. A. T. (2007). Using FlyAtlas to identify better Drosophila models of human disease. <a href=http://www.nature.com/ng/journal/v39/n6/abs/ng2049.html target=_blank><i>Nature Genetics</i> 39: 715-720</a></font></P>";
   print "<div id=\"clustrmaps-widget\"></div><script type=\"text/javascript\">var _clustrmaps = {\'url\' : \'http://flyatlas.org\', \'user\' : 1164985, \'server\' : \'3\', \'id\' : \'clustrmaps-widget\', \'version\' : 1, \'date\' : \'2015-03-31\', \'lang\' : \'en\', \'corners\' : \'square\' };(function (){ var s = document.createElement(\'script\'); s.type = \'text/javascript\'; s.async = true; s.src = \'http://www3.clustrmaps.com/counter/map.js\'; var x = document.getElementsByTagName(\'script\')[0]; x.parentNode.insertBefore(s, x);})();</script><noscript><a href=\"http://www3.clustrmaps.com/user/15111c6b9\"><img src=\"http://www3.clustrmaps.com/stats/maps-no_clusters/flyatlas.org-thumb.jpg\" alt=\"Locations of visitors to this page\" /></a></noscript>";
   " /></a>";
   print "<a href=\'http://host-tracker.com/\' onMouseOver=\'this.href=\"http://host-tracker.com/website-monitoring-stats/3260065/lvuc/\";\'><img width=88 height=31 border=0 alt=\'measure downtime\' src=\"http://ext.host-tracker.com/uptime-img/?s=31&amp;t=3260065&amp;m=00.09&amp;p=Total&amp;src=lvuc\"></a><noscript><a href=\'http://host-tracker.com/\' >website testing</a></noscript>",br;
   print end_html;
}