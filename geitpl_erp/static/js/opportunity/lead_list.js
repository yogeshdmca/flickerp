var leadOptions = {
	success:showLeadResponse  // post-submit callback	
}

var LeadschedularOptions = {
	success:showLeadSchedularResponse
}

status_data = [{'value':'1','text':'Close'},
			{'value':'2','text':'Create Estimation'},
			{'value':'3','text':'Next Schedule'}];

function showLeadResponse(responseText, statusText, xhr, $form){
	if(responseText.success == 1){
		location.reload();
	}else{
		$('#lead-modal .modal-body').html($.parseHTML(responseText.html));
		$('#id_lead_create_form').ajaxForm(leadOptions);
		intialize_datepicker();
	}
}

function showLeadSchedularResponse(responseText, statusText, xhr, $form){
	if(responseText.success ==1){
		if(responseText.action == 'reload'){
			location.reload();
		}else if(responseText.action == 'create_lead'){
			$('#lead-update-modal').modal('hide');
			/*url = $('#lead-modal').data('url');
			opportunity_id = responseText.opp_obj_id;
			$.get(url, {'opportunity_id':opportunity_id}, function(response){
				$('#lead-modal .modal-body').html($.parseHTML(response));
				$('#lead-modal').modal();
				$('#id_lead_create_form').ajaxForm(leadOptions);
				intialize_datepicker();
			});*/
		}
	}
}

$(function(){
	$('#user-select').hierarchySelect({
	    width: 300
	});

	
	$('#id_lead_create_form').ajaxForm(leadOptions);
	intialize_datepicker();

	$('.lead-show').click(function(){
		url = $(this).data('url');
		lead_id = $(this).data('lead_id');
		$.get(url, {'lead_id':lead_id}, function(response){
			$('#lead-show-modal .modal-body').html($.parseHTML(response));
			$('#lead-show-modal').modal();
		});
	});

	$('.update_lead').editable({
		title: "Update Lead",
        name: "lead_schedule",
        source: status_data,
        savenochange: false,
        inputclass: 'lead_status-select',
        validate: function(value){
            $('#id_schedule_id').val($(this).data('schedular_id'));
            $('#id_lead_id').val($(this).data('lead_id'));
            $('#id_scheduler_result').val(value);
            if(value == '1' || value == '2'){
            	$('#id_call_schedule_block').hide();
            }else if(value == '3'){
            	$('#id_call_schedule_block').show();
            }
         	$('#lead-update-modal').modal();
         	return 'Processing...'
        },
        success: function(response, newValue) {
            location.reload();
        }
	});

    $(document).on('click', '.editable-submit', function(e) {
        e.preventDefault();
        var opportunity_update = $(this);
        
        if($('.lead_status').length > 0) {
            status = parseInt($('.lead_status-select')[0].value);
        } else {
            status = null;
        }
        opportunity_update.submit();
    });

    $('#id_lead_next_schedule_form').ajaxForm(LeadschedularOptions)

});