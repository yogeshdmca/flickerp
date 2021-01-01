$(function(){
    $('.delete-record').click(function(e){
        e.preventDefault();
        object = $(this);
        record_name = object.data('name');
        record_module_name = object.data('modulename');
        record_id = object.data('pk');
        url = object[0].href;
        bootbox.confirm({
            message: "Are You Sure, You realy want to delete?", 
            size: "small", 
            callback: function(result) {
            if(result) {
                data = {'pk': record_id};
                $.post(url, data, function(result){
                    if(result.success) {
                        toastr.success(result.message);
                        location.reload();
                    } else {
                        toastr.error(result.message);
                    }
                });
            }
        }
    });
    });

    $('.approve-timeheet').click(function(e){
        e.preventDefault();
        object = $(this);
        record_id = object.data('pk');
        url = object[0].href;
        bootbox.confirm({
            message:"Approve timesheet, are  you sure?",
            size: "small",
            callback : function(result) {
            if(result) {
                data = {'pk': record_id};
                $.post(url, data, function(result){
                    if(result.success) {
                        toastr.success(result.message);
                        object.parents('tr').remove()
                    } else {
                        toastr.error(result.message);
                    }
                });
            }
        }
    });
    });

    $('.approve-miss-punch').click(function(e){
        e.preventDefault();
        object = $(this);
        record_id = object.data('pk');
        url = object[0].href;
        bootbox.confirm({
            message: "Approve miss punch, are you sure?", 
            size: "small", 
            callback: function(result) {
            if(result) {
                data = {'pk': record_id};
                $.post(url, data, function(result){
                    if(result.success) {
                        toastr.success(result.message);
                        location.reload();
                    } else {
                        toastr.error(result.message);
                    }
                });
            }
        }
    });
    });

    $('.reject-miss-punch').click(function(e){
        e.preventDefault();
        object = $(this);
        record_id = object.data('pk');
        url = object[0].href;
        bootbox.confirm({
            message:"Reject Miss Punch, are  you sure?",
            size: "small",
            callback : function(result) {
            if(result) {
                data = {'pk': record_id};
                $.post(url, data, function(result){
                    if(result.success) {
                        toastr.success(result.message);
                        object.parents('tr').remove()
                    } else {
                        toastr.error(result.message);
                    }
                });
            }
        }
    });
    });
});





