/* ==========================================================================
   dialpad.js
   ========================================================================== */
// var $ = jQuery.noConflict();

$(function(){
    var dialpad_obj = [];
    $('#show-dialpad').click(function(e) {
        e.preventDefault();
        if(dialpad_obj.length != 0) {
            dialpad_obj.close();
            dialpad_obj = [];
            $('#show-dialpad').removeClass('active');
        } else {
            dialpad_obj = $.jsPanel({
                container:   "#wrapper",
                position:    {my: 'right-top', at: 'right-top', offsetX: 0, offsetY: 50},
                headerTitle: "Dialpad",
                theme:       "teal",
                content:     dialpad_html(),
                resizable:  { disabled:  true },
                contentSize:  { width: 250, height: 340 },
                headerControls: { maximize: "remove" },
                callback:    function () {
                    this.content.css("padding", "5px");
                }, onclosed: function(){
                    dialpad_obj = [];
                    $('#show-dialpad').removeClass('active');
                }
            });
            $('#show-dialpad').addClass('active');
        }
    });
    var dials = $('.dials ol li');
    var index;
    var number = '';
    var total;
    var call_input = $('#innum');

    $('#wrapper').on('click', '.dials ol li', function(event) {
        var pElement = $(event.toElement);
        index = pElement.data('value');

        char_array = ['*','#'];   
             
        if((index >= 0 && index <= 14) || char_array.indexOf(index) > -1) {
            if(index == 12){
                number = "";
            } else if(index == 13) {
                total = number;
                total = total.slice(0,-1);
                number = "";
                number = total;
            } else if(index == 14) {
                var liElement = pElement.parent();
                var call_status = $('.timer');
                if(liElement.hasClass('dialpad-call')) {
                    $('#call-text').text('Hang Up');
                    liElement.removeClass('dialpad-call');
                    liElement.addClass('dialpad-hangup');
                    callCustomer(number, call_status);
                    number = '';
                } else {
                    end_call();
                }
            } else {
                number += index;
                send_IVR_options(index);
            }
        }
        $('#innum').val(number);
    });

    $('#wrapper').on('keyup', call_input, function() {
        number = $('#innum').val();
    });
});

function end_call() {
    $('#call-text').text('Call');
    $('#call-text').parent().removeClass('dialpad-hangup');
    $('#call-text').parent().addClass('dialpad-call');
    hangUp();
}

function dialpad_html () {
    if(connection_obj == null){
        html = '<div class="dialpad"><div class="dialPad compact div-down"><div class="number"><input id="innum" type="text" style="width: 100%;" maxlength="15"></div><div class="timer" style="color:white"></div><div class="dials"><ol><li class="digits"><p class="strong-dial" data-value="1">1</p></li><li class="digits"><p class="strong-dial" data-value="2" >2<sup>abc</sup></p></li><li class="digits"><p class="strong-dial" data-value="3">3<sup>def</sup></p></li><li class="digits"><p class="strong-dial" data-value="4">4<sup>ghi</sup></p></li><li class="digits"><p class="strong-dial" data-value="5">5<sup>jkl</sup></p></li><li class="digits"><p class="strong-dial" data-value="6">6<sup>mno</sup></p></li><li class="digits"><p class="strong-dial" data-value="7">7<sup>pqrs</sup></p></li><li class="digits"><p class="strong-dial" data-value="8">8<sup>tuv</sup></p></li><li class="digits"><p class="strong-dial" data-value="9">9<sup>wxyz</sup></p></li><li class="digits"><p class="strong-dial" data-value="*">*</p></li><li class="digits"><p class="strong-dial" data-value="0">0</p></li><li class="digits"><p class="strong-dial" data-value="#">#</p></li><li class="digits"><p class="strong-dial strong-dial-option" data-value="13">Clear</p></li><li class="digits"><p class="strong-dial strong-dial-option" data-value="12">Delete</p></li><li class="digits dialpad-btn dialpad-call pad-action"><p class="strong-dial strong-dial-option" data-value="14" id="call-text">Call</p></li></ol></div></div></div>';        
    } else{
        html = '<div class="dialpad"><div class="dialPad compact div-down"><div class="number"><input id="innum" type="text" style="width: 100%;" maxlength="15"></div><div class="timer" style="color:white"></div><div class="dials"><ol><li class="digits"><p class="strong-dial" data-value="1">1</p></li><li class="digits"><p class="strong-dial" data-value="2" >2<sup>abc</sup></p></li><li class="digits"><p class="strong-dial" data-value="3">3<sup>def</sup></p></li><li class="digits"><p class="strong-dial" data-value="4">4<sup>ghi</sup></p></li><li class="digits"><p class="strong-dial" data-value="5">5<sup>jkl</sup></p></li><li class="digits"><p class="strong-dial" data-value="6">6<sup>mno</sup></p></li><li class="digits"><p class="strong-dial" data-value="7">7<sup>pqrs</sup></p></li><li class="digits"><p class="strong-dial" data-value="8">8<sup>tuv</sup></p></li><li class="digits"><p class="strong-dial" data-value="9">9<sup>wxyz</sup></p></li><li class="digits"><p class="strong-dial" data-value="*">*</p></li><li class="digits"><p class="strong-dial" data-value="0">0</p></li><li class="digits"><p class="strong-dial" data-value="#">#</p></li><li class="digits"><p class="strong-dial strong-dial-option" data-value="13">Clear</p></li><li class="digits"><p class="strong-dial strong-dial-option" data-value="12">Delete</p></li><li class="digits dialpad-btn dialpad-call pad-action"></li></ol></div></div></div>';
    }
    
    
    return html;
}