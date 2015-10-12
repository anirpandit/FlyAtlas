package Subs;

require Exporter;
  my @ISA = qw(Exporter);

sub roundup { 
    my $n = shift; 
    return (($n == int($n)) ? $n : int($n + 0.5));

} 

sub getAbunCol {
    my $Abundance = shift; my($logVal,$red,$green,$blue,$bkcell,$textcell); 
    $logVal = log($Abundance)/log(2);  
    $red = Subs::roundup(255 - ($logVal * 255) / 15); 
    if ($red > 255) {
        $red = 255; 
    } 
    $green = $red; $blue = $red; 

    $bkcell = "rgb($red,$green,$blue)";
    
    $textcell = "#FFFFFF" ; if($Abundance < 200){$textcell = "#000000"; } 
    return ($bkcell,$textcell) ; 
}
   
sub getEnrichCol {
    my $Enrichment = shift;  
    my ($red,$green,$blue,$logVal,$bkcelle,$textcelle);
    my $base=1.55; my $numHighSteps = 7; my $numLowSteps = 4; my $gbRange = 210;

    if($Enrichment > ($base**$numHighSteps)) {
        $logVal = log($Enrichment)/log(1.55); 
        $green = 230 - $gbRange; $blue = $green; 
        $red = Subs::roundup(250 - ($logVal*50)/15); 
        $bkcelle = "rgb($red,$green,$blue)";
    } 
    elsif($Enrichment > 1){ 
        $logVal = log($Enrichment)/log(1.55);  
        $red = Subs::roundup(255 - ($logVal * 5)/7); 
        $green = Subs::roundup(255 - ($logVal * 230)/7); 
        $blue = Subs::roundup(40 - ($logVal * 15)/7); 
        $bkcelle = "rgb($red,$green,$blue)";
    }
    elsif($Enrichment == 1){ 
        $red = 255; 
        $green = 255; 
        $blue = 40;  
        $bkcelle = "rgb($red,$green,$blue)"; 
        }
    elsif($Enrichment < 1 && $Enrichment > 0 ) { 
        if($Enrichment < 0) { 
            $Enrichment = 0; $logVal = 0;
        } 
        else { 
            $logVal = log($Enrichment) / log(1.8); 
        }

        my $bDecrement = ($logVal*215) / 4;
        if($bDecrement < -215) { $bDecrement = -215; }
        
        $red = 255; 
        $green = 255; 
        $blue = Subs::roundup(40 - $bDecrement); 
        $bkcelle = "rgb($red,$green,$blue)";
    }
    
    $textcelle = "#FFFFFF" ; if($Enrichment < 15){$textcelle = "#000000"; }
    return ($bkcelle,$textcelle);
}

sub ext_links_modal{

    my $FBID= shift;
    my $CGID= shift;
    
    $elmodal=qq~
    <div class="modal" id="ext_links">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
                    <h4 class="modal-title"><span class="glyphicon glyphicon-link"></span> External Fly Resources</h4>
                </div> 
    
                <div class="modal-body">
                    <h5>Gene : $FBID / $CGID </h5>
                    <p>Please use the following links to query external fly resources for this <em>Drosophila</em> gene. </p>
                    <table class="table table-extl">
                        <thead>
                            <tr>
                                <th>Link</th>
                                <th>Resource</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><a href="http://flybase.org/reports/$FBID.html" target="_blank" class="btn btn-one round btn-extl"><span class="glyphicon glyphicon-link"></span> FlyBase</a></td>
                                <td><strong>FlyBase</strong>: The Database for Drosophila genetics and molecular biology</td>
                            </tr>
                            <tr>
                                <td><a href="http://www.flymine.org/query/portal.do?origin=flybase&class=gene&externalid=$FBID" target="_blank" class="btn btn-one round btn-extl"><span class="glyphicon glyphicon-link"></span> FlyMine</a></td>
                                <td><strong>FlyMine</strong>: An integrated database for Drosophila and Anopheles genomics</td>
                            </tr>
                            <tr>
                                <td><a href="http://insitu.fruitfly.org/cgi-bin/ex/search.pl?ftype=2&ftext=$FBID" target="_blank" class="btn btn-one round btn-extl"><span class="glyphicon glyphicon-link"></span> BDGP</a></td>
                                <td><strong>BDGP</strong>: Berkley <em>Drosophila</em> gene project (Patterns of gene expression in embryogenesis)</td>
                            </tr>
                            <tr>
                                <td><a href="http://thebiogrid.org/search.php?organism=7227&amp;search=$FBID" target="_blank" class="btn btn-one round btn-extl"><span class="glyphicon glyphicon-link"></span> BioGRID</a></td>
                                <td><strong>BioGRID</strong>: Biological General Repository for Interaction Databases</td>
                            </tr>
                            <tr>
                                <td><a href="http://stockcenter.vdrc.at/control/checkAdvancedSearch?VIEW_SIZE=100&amp;SEARCH_CATEGORY_ID=VDRC_All&amp;fb_number=$FBID" target="_blank" class="btn btn-one round btn-extl"><span class="glyphicon glyphicon-link"></span> VDRC</a></td>
                                <td><strong>VDRC</strong>: Vienna <em>Drosophila</em> and RNAi Centre</td>
                            </tr>
                            <tr>
                                <td><a href="http://www.flyrnai.org/cgi-bin/DRSC_gene_lookup.pl?gname=$FBID" target="_blank" class="btn btn-one round btn-extl"><span class="glyphicon glyphicon-link"></span> DRSC</a></td>
                                <td><strong>DRSC</strong>: <em>Drosophila</em> RNAi Screening Centre, at Harvard Medical School</td>
                            </tr>   
                            <tr>
                                <td><a href="http://amigo1.geneontology.org/cgi-bin/amigo/gp-details.cgi?gp=FB:$FBID" target="_blank" class="btn btn-one round btn-extl"><span class="glyphicon glyphicon-link"></span> Amigo</a></td>
                                <td><strong>Amigo</strong>: Gene Ontology Information</td>
                            </tr>     
                        </tbody>
                    </table>
                </div>
    
                <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
    ~;
    
    return ($elmodal);
}

1;