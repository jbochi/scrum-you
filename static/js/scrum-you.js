function onUpdateSort(event, ui) {
	var id, prev_order, next_order, new_order;
	id = $(ui.item).attr('id');
	prev_order = $(ui.item).prev().attr('order');
	next_order = $(ui.item).next().attr('order');
	
	if (next_order === undefined && prev_order === undefined) {
		return false;
	} else if (next_order === undefined) {
		new_order = new Date().getTime(); 		 //last item -> now
	} else if (prev_order === undefined) {
		new_order = next_order - 1000;   		 //fist item -> previous first - 1s
	} else {
		new_order = prev_order/2 + next_order/2; //average between previous and next
	}
	
	$(ui.item).attr('order', new_order);
	$.post('/update_order/', {'id': id, 'order': new_order});
}

function completeTask(id, completed) {
	var span_tag = $("#" + id + " span.taskName");
	if (completed) {
		span_tag.addClass('completed');
	} else {
		span_tag.removeClass('completed');
	}
	$.post('/complete/', {'id': id, 'completed': completed});
}

function editTask(id, name) {
    $.post('/edit/', {'id': id, 'name': name});
}

function deleteTask(e) {
	$.post('/delete/', {'id': id});	
    $('#' + id).remove();
}

$(document).ready(function(){
		$("#todo").sortable({
			handle: '.handle',  
			cursor: 'move',
			update: onUpdateSort
		});

		$(".check").click(function (e) {
			completeTask(e.target.parentNode.id, $(e.target).attr('checked'));
		});
		
		$('.editable').inlineEdit({
            save: function(e, data) {
                editTask(e.target.parentNode.parentNode.id, data.value);
            }
        });
		
		$("#todo a.del").click(function (e) {
            deleteTask(e.target.parentNode.parentNode.id);
		});
		
		$("#todo").disableSelection();
});