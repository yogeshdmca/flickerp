/**
 * Twilio Client configuration for the browser-calls-django
 * example application.
 */

// Store some selectors for elements we'll reuse
var connection_obj = null;
var callStatus = $(".call-status");
var callButton;
var from_dialpad = false;

// Initialize variables for use when create call history
var start_datetime;
var prospect_id;
var agency_calling_for;
var agent_id;
var call_history_create_url;
var csrf_token;

$(document).on('click', '#call-text', function(){
    prospect_id = "";
    agency_calling_for = "";
    agent_id = "";
});

/* Helper function to update the call status bar */
function updateCallStatus(status) {
    if (callStatus.length > 0) {
        callStatus.text(status);
    } else {
        callStatus.textContent = status;
    }
}

/* Get a Twilio Client token with an AJAX request */
$(document).ready(function() {
    csrf_token = $('csrftoken').data('csrf');
    call_history_create_url = $('callhistorycreateurl').data('url');
    $.get("/support/token", {forPage: window.location.pathname}, function(data) {
        // Set up the Twilio Client Device with the token
        Twilio.Device.setup(data.token);
    });
});

/* Callback to let us know Twilio Client is ready */
Twilio.Device.ready(function (device) {
    updateCallStatus("Ready");
    /* Callback to determine if "support_agent" is available or not */
    // Twilio.Device.presence(function(presenceEvent) {
    //     if (presenceEvent.from === 'support_agent') {
    //         if (presenceEvent.available) {
    //             $("#support-unavailable").hide();
    //         } else {
    //             $("#support-unavailable").show();
    //         }
    //     }
    // });
});

/* Report any errors to the call status display */
Twilio.Device.error(function (error) {
    // updateCallStatus("ERROR: " + error.message);
    $.get("/support/token", {forPage: window.location.pathname}, function(data) {
        // Set up the Twilio Client Device with the token
        Twilio.Device.setup(data.token);
    });
});


/* Callback for when Twilio Client initiates a new connection */
Twilio.Device.connect(function (connection) {
    try {
        on_call(connection);
        change_stop_timer(true); // call function from custom_timer.js
        reset_idle_time(); // call function from custom_timer.js
    } catch(err) {

    }
    // If phoneNumber is part of the connection, this is a call from a
    // support agent to a customer's phone
    if ("phoneNumber" in connection.message) {
        // updateCallStatus("In call with " + connection.message.phoneNumber);
        updateCallStatus("In call");
    } else {
        // This is a call from a website user to a support agent
        updateCallStatus("In call with support");
    }

    start_datetime = new Date().toISOString(); // update start_datetime value with current time when call start
});

/* Callback for when a call ends */
Twilio.Device.disconnect(function(connection) {
    // callButton.toggleClass('custom-call').toggleClass('custom-hangup');
    is_recorded  = $('#show-dialpad').data('record');
    var end_datetime = new Date().toISOString(); // update end datetime value with current time when call end
    try{
        update_call_details(connection.message.phoneNumber, start_datetime, end_datetime, csrf_token, connection_obj.parameters.CallSid, is_recorded);
    } catch(err){
        if(err.name == 'ReferenceError') {
            var data = {'phone_number': connection.message.phoneNumber, 'prospect_id': prospect_id, 'agent_id': agent_id, 'agency_calling_for':agency_calling_for, 'start_datetime': start_datetime, 'end_datetime': end_datetime, 'csrfmiddlewaretoken': csrf_token, 'call_sid':connection_obj.parameters.CallSid, 'is_recorded':is_recorded};
            $.ajax({
                url: call_history_create_url,
                type:"POST",
                data: data,
            });
        }
    }
    connection_obj = null;
    updateCallStatus("Ready");
    end_call(); // function called from dialpad.js
});

/* Callback for when Twilio Client receives a new incoming call */
Twilio.Device.incoming(function(connection) {
    updateCallStatus("Incoming support call");

    // Set a callback to be executed when the connection is accepted
    connection.accept(function() {
        updateCallStatus("In call with customer");
    });
});

$(document).on('click','.call-btn',function(){
    // Store current call button element
    callButton = $(this);

    // Set call status update element for calling button
    callStatus = $(this)[0].nextElementSibling;

    if($(this).hasClass('custom-call')) {
        var record = false;
        var phoneNumber = $(this).attr('data');
        var campaign_cid = $(this).data('campaign_cid');
        option  = $('#show-dialpad').data('record');
        callCustomer(phoneNumber, callStatus, campaign_cid, option);
    } else {
        // get values in local variables for calculation
        p_id = $('datatag').data('prospectid');   // prospect_id
        acf = $('datatag').data('campaignid');    // campaign_id or agency_calling_for
        a_id = $('datatag').data('agentid');      // agent_id
        this_value = $(this).attr('value');  // call_button value

        //  Set values when click call button
        prospect_id = (p_id > 0) ? p_id : (this_value > 0) ? this_value : '';
        agency_calling_for = (acf > 0) ? acf : '';
        agent_id = (a_id > 0) ? a_id : '';

        hangUp();
    }
    $(this).toggleClass('custom-call').toggleClass('custom-hangup');
});

/* Call a customer from a support ticket */
function callCustomer(phoneNumber, call_status, campaign_cid, record) {
    callStatus = call_status;
    updateCallStatus("Calling " + phoneNumber + "...");

    var params = {"campaign_cid":campaign_cid, "phoneNumber": phoneNumber, "record":record, 'csrfmiddlewaretoken': csrf_token};
    Twilio.Device.connect(params);
}

/* Call the support_agent from the home page */
function callSupport() {
    updateCallStatus("Calling support...");

    // Our backend will assume that no params means a call to support_agent
    Twilio.Device.connect();
}

/* End a call */
function hangUp() {
    Twilio.Device.disconnectAll();
    updateCallStatus("Ready");
}

function on_call(connection){
    connection_obj = connection;
}

function send_IVR_options(digit){
    if (connection_obj != null){
        digit = digit + ''
        connection_obj.sendDigits(digit);
    }
}