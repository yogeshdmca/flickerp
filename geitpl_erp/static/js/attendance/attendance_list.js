$(function(){
	$('.view_attendance').click(function(e){
		e.preventDefault();
		url = $(this).data('url');
		attendance_id = $(this).data('attendance_id');

		$.get(url, {'attendance_id':attendance_id}, function(response){
			$('#attendance-detail-modal .modal-body').html($.parseHTML(response));
			$('#attendance-detail-modal').modal();
			intialize_comment_editable();
		});
	}); 

	$(document).on('click', '.add-miss-punch', function(e){
		miss_punch_form = '<div class="col-lg-12"><form><div class="col-md-3"><input name="in_time" type="time" class="timepicker form-control form-inline"></div><div class="col-md-3"><input type="time" name="out_time" class="timepicker form-control form-inline"></div><div class="col-md-3"><input type="text" name="comment" class="form-control form-inline"></div><div class="col-md-1"><button type="button" class="btn btn-success save_miss_punch">Save</button></div><form></div>';
		$('#miss-punch').html(miss_punch_form);

		// $('.timepicker').datetimepicker({
		//     format: 'LT'
		// });
	});

	$(document).on('click', '.save_miss_punch', function(){
		form = $(this).closest('form')
		url = $('#miss-punch').data('url');
		$.post(url, form.serialize(), function(response){
			alert(response.msg)
			$('#miss-punch').html('');
			$('#att_detailed_logs tbody').append(response.html_response);
		});
	});
});

function intialize_comment_editable(){
	$('.add-comment').editable({
		title: "Add Comment",
        name: "comment",
	});
}
