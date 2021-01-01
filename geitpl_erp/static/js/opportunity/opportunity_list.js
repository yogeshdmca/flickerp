
$('body').on('hidden.bs.modal', '.modal', function () {
$(this).removeData('bs.modal');
});

$('#user-select').hierarchySelect({
	width: 300
});


$( document ).on( 'focus', ':input', function(){
    $( this ).attr( 'autocomplete', 'off' );
});


$(document).on("click", "#prospect-call-result-new-btn", function(){
	$("#prospect-call-result-new").submit()

});

function prospectCallResultNew(responseText, statusText, xhr, $form){
	if(responseText.success == 1){
		location.reload();
	}else{
		$('#opportunity-modelpopup .modal-content').html(responseText);
	}
};




$(document).on("click", "#sales-opportunity-update-btn-save", function(){
	$("#sales-opportunity-update-form").submit();

});

function prospectUpdateForm(responseText, statusText, xhr, $form){
	if(xhr.status == 212){
		location.reload();
	}else if (xhr.status == 222){
		$('##opportunity-modelpopup .modal-content').html(responseText);
	}
};


$(document).on("click", "#sales-opportunity-create-btn-save", function(){
	$("#sales-opportunity-create-form").submit();

});

function prospectCreateForm(responseText, statusText, xhr, $form){
	if(xhr.status == 212){
		location.reload();
	}else if (xhr.status == 222){
		$('#opportunity-modelpopup .modal-content').html(responseText);
	}
};







/*var options = { 
    success:showOpportunityResponse  // post-submit callback
};

var leadOptions = {
	success:showLeadResponse  // post-submit callback	
}

var schedularOptions = {
	success:showSchedularResponse
}



/*function showOpportunityResponse(responseText, statusText, xhr, $form){
	if(responseText.success == 1){
		//location.reload();
		debugger
	}else{
		$('#opportunity-modal .modal-body').html($.parseHTML(responseText.html));
		$('#id_opportunity_create_form').ajaxForm(options);
		intialize_datepicker();
	}
}
*/
/*function showLeadResponse(responseText, statusText, xhr, $form){
	if(responseText.success == 1){
		//location.reload();
	}else{
		$('#lead-modal .modal-body').html($.parseHTML(responseText.html));
        $('#id_lead_create_form').ajaxForm(leadOptions);
		intialize_datepicker();
	}
}*/

/*function showSchedularResponse(responseText, statusText, xhr, $form){
	if(responseText.success ==1){
		if(responseText.action == 'reload'){
			//debugger
			location.reload();
		}else if(responseText.action == 'create_lead'){
			$('#opportunity-update-modal').modal('hide');
			url = $('#lead-modal').data('url');
			opportunity_id = responseText.opp_obj_id;
			$.get(url, {'opportunity_id':opportunity_id}, function(response){
				$('#lead-modal .modal-body').html($.parseHTML(response));
				$('#lead-modal').modal();
                $('#id_lead_create_form').ajaxForm(leadOptions);
				intialize_datepicker();
			});
		}
	}
}*/

/*status_data = [
			{'value':'1','text':'Close'},
			{'value':'2','text':'Create Lead'},
			{'value':'3','text':'Next Schedule'}];*/

/*$(function(){
	$('#user-select').hierarchySelect({
	    width: 300
	});

	$('#id_opportunity_create_form').ajaxForm(options);
	intialize_datepicker();*/

/*	$('.show-lead-form').click(function(){
		url = $(this).data('url');
		opportunity_id = $(this).data('opportunity_id');
		$.get(url, {'opportunity_id':opportunity_id}, function(response){
			$('#lead-modal .modal-body').html($.parseHTML(response));
			$('#lead-modal').modal();
			$('#id_lead_create_form').ajaxForm(leadOptions);
			intialize_datepicker();
		});
	});*/

/*
	$('.show-opportunity').click(function(){
		url = $(this).data('url');
		opportunity_id = $(this).data('opportunity_id');
		$.get(url, {'opportunity_id':opportunity_id}, function(response){
			$('#opportunity-show-modal .modal-body').html($.parseHTML(response));
			$('#opportunity-show-modal').modal();
		});
	});*/


/*	$('.update_opportunity').editable({
		title: "Update Opportunity",
        name: "opportunity_schedule",
        source: status_data,
        savenochange: false,
        inputclass: 'opportunity_status-select',
        validate: function(value){
            $('#id_schedule_id').val($(this).data('schedular_id'));
            $('#id_opportunity_id').val($(this).data('opportunity_id'));
            $('#id_scheduler_result').val(value);
            if(value == '1' || value == '2'){
            	$('#id_call_schedule_block').hide();
            }else if(value == '3'){
            	$('#id_call_schedule_block').show();
            }
         	$('#opportunity-update-modal').modal();
         	return 'Processing...'
        },
        success: function(response, newValue) {
            //location.reload();
        }
	});*/

	//$('#id_opportunity_next_schedule_form').ajaxForm(schedularOptions);

/*});*/