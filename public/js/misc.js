       
//For message alerts at top of page//
$(document).ready(function() {

	//Tooltip Jquery//
	$('[data-toggle="tooltip"]').tooltip(); 

	$(".alert").delay(4000).slideUp(200, function() {
    	$(this).alert('close');
	});
	
	$('table.display').DataTable();
	
	$("#IsoformName").change(function(){
		$("#message").html('<div class="cssload-loader"><div class="cssload-inner cssload-one"></div><div class="cssload-inner cssload-two"></div>	<div class="cssload-inner cssload-three"></div></div> checking...');
             
 		var IsoformName=$("#IsoformName").val();
 
		$.ajax({
			type:"post",
			url:"/check",
			data:"IsoformName="+IsoformName,
			success:function(data){
				if(data==0){
					$("#message").html('');
				}
				else{
					$("#message").html('<div class="alert alert-danger"><span class="glyphicon glyphicon-remove"></span> Isoform Name already taken. Please use another one or there will be errors in the data. </div>');
				}
			}
		});
 
	});

});

//For scrolling to element seamlessly//
$('a[href^="#"]').on('click', function(event) {

    var target = $( $(this).attr('href') );

    if( target.length ) {
        event.preventDefault();
        $('html, body').animate({
            scrollTop: target.offset().top
        }, 1000);
    }

});

//Code for Chosen Jquery plugin//
var config = {
    '.chosen-select'           : {},
    '.chosen-select-deselect'  : {allow_single_deselect:true},
	'.chosen-select-no-single' : {disable_search_threshold:10},
	'.chosen-select-no-results': {no_results_text:'Oops, nothing found!'},
	'.chosen-select-width'     : {width:"95%"}
}
for (var selector in config) {
	$(selector).chosen(config[selector]);
}

//Validation for checkboxes//
function checkFields(form) {
        var checks_radios = form.find(':checkbox, :radio'),
            inputs = form.find(':input').not(checks_radios).not('[type="submit"],[type="button"],[type="reset"]'); 
        
        var checked = checks_radios.filter(':checked');
        var filled = inputs.filter(function(){
            return $.trim($(this).val()).length > 0;
        });
        
        if(checked.length + filled.length === 0) {
            return false;
        }
        
        return true;
    }
    

//For Thumbnail Carousel//    
$(function() {
    $("#rondellThumbnails").rondell({
      preset: "thumbGallery"
    });
});


//For validation of the search form radio buttons//
    $( "#genesearchform" ).validate({
      errorPlacement: function(error, element) {
        if (element.attr("id") == "geneopt1") {
          error.insertBefore("#error");
        }
      }
    });

    $.validator.addMethod("require_from_group", $.validator.methods.require_from_group, 'Please select at least one of the following options: ');

    $.validator.addClassRules("searchformval", {
        require_from_group: [1, ".searchformval"]
    });