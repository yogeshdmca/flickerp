/*var leadOptions = {
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
            // url = $('#lead-modal').data('url');
            // opportunity_id = responseText.opp_obj_id;
            // $.get(url, {'opportunity_id':opportunity_id}, function(response){
            //  $('#lead-modal .modal-body').html($.parseHTML(response));
            //  $('#lead-modal').modal();
            //  $('#id_lead_create_form').ajaxForm(leadOptions);
            //  intialize_datepicker();
            // });
        }
    }
}*/

$(function(){
    $('#user-select').hierarchySelect({
        width: 500
    });

    
    /*$('#id_lead_create_form').ajaxForm(leadOptions);
    intialize_datepicker();*/

    $('.contract-show').click(function(){
        url = $(this).data('url');
        contract_id = $(this).data('contract_id');
        $.get(url, {'contract_id':contract_id}, function(response){
            $('#contract-show-modal .modal-body').html($.parseHTML(response));
            $('#contract-show-modal').modal();
        });
    });

     $('.contract_detail_update').editable({
        title: "Update contract detail",
        placement: "bottom",
        inputclass: 'status_text',
    });

    $('.contract_status_update').editable({
        title: "Update contract Status",
        name: "is_active",
        inputclass: 'status_select',
        source: [
            {value: 'True', text: "Active"},
            {value: 'False', text: "Inactive"}
        ],
    });

    $('.contract_date_update').editable({
        placement: "left",
        title: "Update expiry date",
        type: 'date',
    })

});