var options = { 
    success:showFamilyMemberResponse  // post-submit callback
};

function showFamilyMemberResponse(responseText, statusText, xhr, $form){
	if(responseText.success == 1){
		location.reload();
	}else{
		$('#family-member-show-modal .modal-body').html($.parseHTML(responseText.html));
		$('#id_family_member_create_form').ajaxForm(options);
	}
}

$(function(){
	$('#id_family_member_create_form').ajaxForm(options);

	$('.add_family_member').click(function(e){
		e.preventDefault();
		$('#family_member_user_id').val($(this).data('user_id'))
		$('#family-member-show-modal').modal();
	});

	$('.show_user').click(function(e){
		e.preventDefault();
		url = $(this).data('url');
		user_id = $(this).data('user_id');
		$.get(url, {'user_id':user_id}, function(response){
			$('#user-show-modal .modal-body').html($.parseHTML(response));
			$('#user-show-modal').modal();
		});
	});
});