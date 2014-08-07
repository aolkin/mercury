$(document).on('change', '.btn-file :file', function() {
    var input = $(this);
    var files = input.get(0).files;
    var label = "";
    for (i = 0; i < files.length; i++) {
	label += files[i].name;
	if (i != files.length -1) {
	    label += ", ";
	}
    }
    input.trigger('fileselect', [label]);
});

$(document).ready( function() {
    $('.btn-file :file').on('fileselect', function(event, label) {
        $(this).parents('.input-group').find(':text').val(label);
    });
});
