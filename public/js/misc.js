       
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


/*!
 * scrollup v2.4.1
 * Url: http://markgoodyear.com/labs/scrollup/
 * Copyright (c) Mark Goodyear — @markgdyr — http://markgoodyear.com
 * License: MIT
 */

!function(l,o,e){"use strict";l.fn.scrollUp=function(o){l.data(e.body,"scrollUp")||(l.data(e.body,"scrollUp",!0),l.fn.scrollUp.init(o))},l.fn.scrollUp.init=function(r){var s,t,c,i,n,a,d,p=l.fn.scrollUp.settings=l.extend({},l.fn.scrollUp.defaults,r),f=!1;switch(d=p.scrollTrigger?l(p.scrollTrigger):l("<a/>",{id:p.scrollName,href:"#top"}),p.scrollTitle&&d.attr("title",p.scrollTitle),d.appendTo("body"),p.scrollImg||p.scrollTrigger||d.html(p.scrollText),d.css({display:"none",position:"fixed",zIndex:p.zIndex}),p.activeOverlay&&l("<div/>",{id:p.scrollName+"-active"}).css({position:"absolute",top:p.scrollDistance+"px",width:"100%",borderTop:"1px dotted"+p.activeOverlay,zIndex:p.zIndex}).appendTo("body"),p.animation){case"fade":s="fadeIn",t="fadeOut",c=p.animationSpeed;break;case"slide":s="slideDown",t="slideUp",c=p.animationSpeed;break;default:s="show",t="hide",c=0}i="top"===p.scrollFrom?p.scrollDistance:l(e).height()-l(o).height()-p.scrollDistance,n=l(o).scroll(function(){l(o).scrollTop()>i?f||(d[s](c),f=!0):f&&(d[t](c),f=!1)}),p.scrollTarget?"number"==typeof p.scrollTarget?a=p.scrollTarget:"string"==typeof p.scrollTarget&&(a=Math.floor(l(p.scrollTarget).offset().top)):a=0,d.click(function(o){o.preventDefault(),l("html, body").animate({scrollTop:a},p.scrollSpeed,p.easingType)})},l.fn.scrollUp.defaults={scrollName:"scrollUp",scrollDistance:300,scrollFrom:"top",scrollSpeed:300,easingType:"linear",animation:"fade",animationSpeed:200,scrollTrigger:!1,scrollTarget:!1,scrollText:"Scroll to top",scrollTitle:!1,scrollImg:!1,activeOverlay:!1,zIndex:2147483647},l.fn.scrollUp.destroy=function(r){l.removeData(e.body,"scrollUp"),l("#"+l.fn.scrollUp.settings.scrollName).remove(),l("#"+l.fn.scrollUp.settings.scrollName+"-active").remove(),l.fn.jquery.split(".")[1]>=7?l(o).off("scroll",r):l(o).unbind("scroll",r)},l.scrollUp=l.fn.scrollUp}(jQuery,window,document);


       $(function () {
            $.scrollUp({
                scrollName: 'scrollUp', // Element ID
                topDistance: '300', // Distance from top before showing element (px)
                topSpeed: 300, // Speed back to top (ms)
                animation: 'fade', // Fade, slide, none
                animationInSpeed: 200, // Animation in speed (ms)
                animationOutSpeed: 200, // Animation out speed (ms)
                scrollText: 'Back to top', // Text for element
                activeOverlay: false, // Set CSS color to display scrollUp active point, e.g '#00FFFF'
            });
        });



/* For Accordion expand all*/
var headers = $('#accordion .accordion-header');
var contentAreas = $('#accordion .ui-accordion-content ').hide()
.first().show().end();
var expandLink = $('.accordion-expand-all');

// add the accordion functionality
headers.click(function() {
    // close all panels
    contentAreas.slideUp();
    // open the appropriate panel
    $(this).next().slideDown();
    // reset Expand all button
    expandLink.text('Expand all')
        .data('isAllOpen', false);
    // stop page scroll
    return false;
});

// hook up the expand/collapse all
expandLink.click(function(){
    var isAllOpen = !$(this).data('isAllOpen');
    console.log({isAllOpen: isAllOpen, contentAreas: contentAreas})
    contentAreas[isAllOpen? 'slideDown': 'slideUp']();
    
    expandLink.text(isAllOpen? 'Collapse All': 'Expand all')
                .data('isAllOpen', isAllOpen);    
});
