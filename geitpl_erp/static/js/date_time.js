$(document).ready(function () {
      $( ".datePicker" ).datetimepicker({
          changeMonth: true,
          changeYear: true,
          autoclose: true,
          format:'MM-DD-YYYY',
          // You can put more options here.
      });
      $('.timePicker').datetimepicker({
          // defaultDate: new Date(),
          changeMonth: true,
          changeYear: true,
          format:'LT',
          autoclose: true,
      });
      $('.datetimePicker').datetimepicker({
          defaultDate: new Date(),
          changeMonth: true,
          changeYear: true,
          format:'YYYY-MM-DD HH:mm:ss',
          autoclose: true,
      });
});