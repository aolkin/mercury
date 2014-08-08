$(document).on('change', '.btn-file :file', function() {
    var input = $(this);
    var files = input.get(0).files;
    var label = "";
    var readers = [];
    for (i = 0; i < files.length; i++) {
	var reader = new FileReader();
	reader.readAsText(files[i]);
	readers.push(reader);

	label += files[i].name;
	if (i != files.length -1) {
	    label += ", ";
	}
    }
    input.data("readers",readers);
    input.trigger('fileselect', [label]);
});

$(document).ready( function() {
    $('.btn-file :file').on('fileselect', function(event, label) {
        $(this).parents('.input-group').find(':text').val(label);
    });
});

$("#websocket-overlay").modal("show");

$.getScript(Mercury.static_path+"/js/codecompetitions/app.js");
