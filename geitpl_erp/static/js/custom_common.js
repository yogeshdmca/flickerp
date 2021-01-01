
/* Run jquery after document is ready */
$(function(){
    /* Initialize Date Picker */
    intialize_datepicker();
    $('.datePicker').datepicker({
        format : "yyyy-mm-dd",
        changeMonth: true,
        changeYear: true,
        autoclose: true,
    });

    /* Initialize Time Picker */
    // $('.timePicker').clockpicker({
    //     twelvehour: true,
    //     autoclose: true,
    // });
    $('.timePicker').datetimepicker({
        pickDate: false,
        format:'hh:mm A',
        twelvehour: true,
        autoclose: true,
    });

    /* Initialize Foo Table */
    // $(".footable").footable({paginate:false});

    /* Initialize Basic Data Table object */
    // $(".object_listing2").DataTable({
    //     scrollCollapse: true,
    //     scrollY: '50vh',
    //     scrollX: true,
    //     info: false,
    //     bLengthChange: false,
    //     paging: false,
    //     searching: false,
    //     destroy: true,
    //     fixedHeader: false,
    //     columnDefs: [
    //        { orderable: false, targets: [0] }
    //     ],
    //     order: [[1, 'asc']],

    // });

    // $(".object_listing_client").DataTable({
    //     scrollCollapse: true,
    //     scrollY: '50vh',
    //     scrollX: true,
    //     info: false,
    //     bLengthChange: false,
    //     paging: false,
    //     searching: true,
    //     destroy: true,
    //     fixedHeader: false
    // });


    // $(".object_listing").DataTable({
    //     info: false,
    //     bLengthChange: false,
    //     paging: false,
    //     searching: false,
    //     destroy: true,
    //     fixedHeader: false,
    //     columnDefs: [
    //        { orderable: false, targets: [0] }
    //     ],
    //     order: [[1, 'asc']],
    // });
});

/* Function to Reset Any Form */
function reset_form () {
    $('form')[0].reset();
}
/* Function End's */

function intialize_datepicker() {
    $('.datetimePicker').datetimepicker({
        // defaultDate: new Date(),
        changeMonth: true,
        changeYear: true,
        format:'MM-DD-YYYY hh:mm A',
        autoclose: true,
    });
}
