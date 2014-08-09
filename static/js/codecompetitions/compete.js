function update_files(e) {
    var input = $(this);
    var files = input.get(0).files;
    var label = "";
    var readers = [];
    for (i = 0; i < files.length; i++) {
	if (files[i].size/1024 > 1024) {
	    Mercury.Modal.alert("<code>" + files[i].name + "</code> is larger than 1 MB! " +
				"That's a bit large for code, so I'm skipping it.",
				"File is Too Large");
	    continue;
	}

	var reader = new FileReader();
	reader.readAsText(files[i]);
	reader.filename = files[i].name;
	readers.push(reader);

	label += files[i].name;
	if (i != files.length -1) {
	    label += ", ";
	}
    }
    input.data("readers",readers);
    input.trigger('fileselect', [label]);
}

$(document).on('change', '.btn-file :file', update_files);

$(document).ready( function() {
    $('.btn-file :file').on('fileselect', function(event, label) {
        $(this).parents('.input-group').find(':text').val(label);
    });
});

$("#websocket-overlay").modal("show");

$.getScript(Mercury.static_path+"/js/codecompetitions/app.js");
