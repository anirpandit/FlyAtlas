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

1;