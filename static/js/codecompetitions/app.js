
function CompetitionApp() {
    this.mode = mode;
    this.cid = cid;
    this.runs = [];
    this.run = null;
    this.running = false;
};

CompetitionApp.prototype = {
    onload: function onload() {
	this._create_ws();
	$("#run-to-view").change(this._select_run);
	$("#source-to-view").change(this._select_source);
	if (this.mode === "compete") {
	    $("#submit-new-code").click(this._submit_code);
	    $("#reload-files").click(function(){
                $("#main-file").trigger("change");
                $("#extra-files").trigger("change");
            });
	} else {
	    $("#player-to-judge").change(this._select_player);
	    $("#update-judgement").click(this._update_judgement);
	}
	if ($("#start-timer").length) {
	    $("#start-timer").click(this._start_timer);
	    $("#stop-timer").click(this._stop_timer);
	}
	$("#request-run").click(this._request_run).attr("disabled",true);
	$("#score-link").click(this._open_scoreboard);
	$(window).on("beforeunload",this._close_scoreboard);

	$.growl(false, {
	    element: ".codecompetitions",
	    placement: { from: "bottom", align: "right" },
	    animate: {
		enter: 'animated fadeInDown',
		exit: 'animated fadeOutRight'
	    },
	    url_target: '_self',
	});
    },
    _open_scoreboard: function open_scoreboard(e) {
	this.scoreboard = open(e.target.href+"?popup=1","scoreboard","height=600,width=800");
	this.scoreboard.focus();
	e.preventDefault();
	return false;
    },
    _close_scoreboard: function close_scoreboard() {
	this.scoreboard.close();
    },
    _start_timer: function start_timer() {
	this.send({clock:"start"});
    },
    _stop_timer: function stop_timer() {
	this.send({clock:"stop"});
    },
    _request_run: function request_run() {
	this.send({request:$("#run-to-view").val()});
    },
    _update_judgement: function update_judgement() {
	if (!$("#run-score").val()) {
	    Mercury.Modal.alert("Please enter a score for this run before saving judgement.",
				"Judgement Missing Score");
	    return false;
	}
	this.send({
	    run: this.run.id,
	    judgement: $(".judgement-title").val(),
	    notes: $(".judgement-notes").val(),
	    score: $("#run-score").val(),
	});
    },
    _submit_code: function submit_code() {
	if (!($("#main-file").data("readers") && $("#main-file").data("readers").length)) {
	    Mercury.Modal.alert("No main file selected! Please select your program's " +
				"main file.", "No File Selected!");
	    return false;
	}
	if ($("#main-file").data("readers")[0].readyState === FileReader.DONE) {
	    var main_file = {
		name: $("#main-file").get(0).files[0].name,
		contents: $("#main-file").data("readers")[0].result
	    }
	} else {
	    Mercury.Modal.alert("Main file has not finished loading. Please wait a moment " +
				"and try again.","Main File Not Finished Loading");
	    return false;
	}
	var unloaded_files = 0;
	var readers = $("#extra-files").data("readers");
	var extra_files = [];
	if (readers) {
	    for (var i = 0; i < readers.length; i++) {
		if (readers[i].readyState === FileReader.DONE) {
		    if (readers[i].filename === main_file.name) {
			Mercury.Modal.alert("An extra file has the same name as your main " +
					    "file. Do not include your main file in your " +
					    "extra files.","Main File Included in Extra Files");
			return false;
		    }
		    extra_files.push({
			name: readers[i].filename,
			contents: readers[i].result
		    });
		} else {
		    unloaded_files += 1;
		}
	    }
	}
	if (unloaded_files > 0) {
	    Mercury.Modal.alert(unloaded_files + " extra " +
				(unloaded_files>1?"files have":"file has") +
				" not finished loading. Please wait a moment " +
				"and try again.","Extra File" + (unloaded_files>1?"s":"") +
				" Not Finished Loading");
	    return false;
	}

	this.data_to_submit = {
	    test_run: $("#is-a-test-run").prop("checked"),
	    language: $("#select-language").val(),
	    main_file: main_file,
	    extra_files: extra_files
	}
	var dialog_code_html = $("#invisible-div").text(main_file.contents).html();
	Mercury.Modal.confirm("<p>Are you sure you want to submit <code>" + main_file.name +
			      "</code> as " + $("#select-language option[value=" +
						 this.data_to_submit.language + "]").text() +
			      (this.data_to_submit.test_run?", as a test run":"") + "?</p>" +
			      '<pre class="cc-dialog-code">' + dialog_code_html + "</pre>",
			      "Submit New " + (this.data_to_submit.test_run?"Test":"") +
			      " Run", this._do_submit);
    },
    _do_submit: function do_submit(perform_action) {
	if (perform_action) {
	    this.send(this.data_to_submit);
	    $(".btn-file :file").val(null).change();
	}
    },
    _load_problem: function load_problem() {
	var parts = decodeURIComponent(location.hash).substr(1).split("-",2);
	var pid = parts[0], second = parts[1], data = {};
	if (second && second.substring(0,2) === "&&") {
	    var run = parseInt(second.substr(2));
	    if (!isNaN(run)) {
		data.echo = {"run": run};
	    }
	}
	if (pid) {
	    $(".problem-name").text("Loading...");
	    $("a.problem-"+pid).parent().addClass("active").siblings().removeClass("active");
	    data.problem = parseInt(pid);
	    this.send(data);
	}
    },
    _select_run: function select_run() {
	$(".disable-until-run").hide();
	$("#request-run").removeAttr("disabled");
	var run = this.runs[$("#run-to-view").val()];
	this.run = run;
	var new_url = "#" + $(".active [data-problem]").data("problem") + "-&&" + run.id;
	if (new_url !== location.href) {
	    //console.log(new_url,location.href);
	    history.pushState(null,null,new_url);
	}
	$(".run-output").text(run.output)
	    .siblings(".alert")[run.has_been_run?"hide":"show"]();
	$(".compile-failure").text(run.compiled_successfully===false?"Compilation Failure":"");
	$(".exit-code").text(run.exit_code);
	$(".runtime").text((run.runtime/1000));
	$("#run-language").text(run.language);
	$(".submitted-after").text(run.time_to_submission?
				   run.time_to_submission.toClockString():"");
	$(".disable-if-test").parent()[run.is_a_test?"hide":"show"]();
	$("#run-score").val(run.score);
	$(".judgement-notes").text(run.notes);
	if (this.mode == "compete") {
	    $(".judgement-title").text(run.judgement);
	} else {
	    $(".judgement-title").val(run.judgement).selectpicker("refresh");
	}

	var selector = $("#source-to-view");
	var selected = selector.val();
	selector.empty();
	$("<option>").text(run.main_file.name).val(run.main_file.contents)
	    .data("subtext","Main File").appendTo(selector);
	for (i in run.extra_files) {
	    $("<option>").text(run.extra_files[i].name)
		.val(run.extra_files[i].contents).appendTo(selector);
	}
	selector.val(selected);
	selector.selectpicker("refresh");
	var has_extra_files = run.extra_files.length > 0;
	$("#sources-title").text(has_extra_files?"Sources":"Source");
	selector.parent()[has_extra_files?"show":"hide"]();
	this._select_source();
    },
    _select_player: function select_player(e,echodata) {
	var data = {player: $("#player-to-judge").val()};
	if (echodata) { data.echo = echodata; }
	this.send(data);
    },
    _select_source: function select_source() {
	$(".run-source").text($("#source-to-view").val());
    },
    _create_ws: function createWS() {
	$("#websocket-overlay").modal("show");
	$("#websocket-overlay-text").text("Connecting...");
	$("#websocket-overlay-icon").removeClass("glyphicon-dashboard")
	    .addClass("glyphicon-signal");
	this.ws = new WebSocket(wsaddress);
	for (i in this._ws_handlers) {
	    this.ws["on"+this._ws_handlers[i]] = this["_ws_"+this._ws_handlers[i]];
	}
    },
    send: function send(obj) {
	this.ws.send(JSON.stringify(obj))
    },
    _ws_message: function onmessage(e) {
	var obj = JSON.parse(e.data);
	if (obj.debug) { console.log(obj); }

	if (obj.error) {
	    if (obj.error === "logged_out") {
		Mercury.Modal.alert("You are no longer logged in. Press okay to re-login.",
				    "Logged Out", location.reload.bind(location));
	    }
	    return false;
	}
	
	if (obj.description !== undefined) {
	    $(".disable-until-problem").hide();
	    $(".problem-description").html(obj.description);
	}
	if (obj.problem_name !== undefined) {
	    $(".problem-name").html(obj.problem_name);
	}
	if (obj.expected_output !== undefined) {
	    $(".expected-output").text(obj.expected_output);
	}
	if (obj.running !== undefined) {
	    $("#contest-state").html(obj.running?"Running":"Stopped" +
				     (this.mode == "compete"?"<br><small>"+
				      "Problem descriptions will become available " +
				      "once the competition is started.</small>":""));
	    $(".disable-until-running")[obj.running?"hide":"show"]();
	    if (this.mode == "compete") {
		$(".upload-disabled-warning")[obj.running?"hide":"show"]();
		$(".upload-panel .panel-body")[obj.running?"show":"hide"]();
	    }
	    this.running = obj.running;
	    if ($("#start-timer").length) {
		if (obj.running) {
		    $("#start-timer").attr("disabled",true);
		    $("#stop-timer").removeAttr("disabled");
		} else {
		    $("#stop-timer").attr("disabled",true);
		    $("#start-timer").removeAttr("disabled");
		}
	    }
	}
	if (obj.time_left !== undefined) {
	    $("#remaining-time").text(obj.time_left.toClockString());
	    if (obj.time_left < 1) {
		$("#contest-state").text("Contest Over");
	    }
	}
	if (obj.players) {
	    var el = $("#player-to-judge");
	    var current_player = el.val();
	    el.empty();
	    for (i in obj.players) {
		$("<option>").attr("value",obj.players[i].id)
		    .text(obj.players[i].first_name + " " + obj.players[i].last_name)
		    .appendTo(el);
	    }
	    el.val(current_player);
	    el.selectpicker("refresh");
	    this._select_player(null,obj.echo);
	}
	if (obj.runs) {
	    this.runs = {};
	    for (i in obj.runs) {
		this.runs[obj.runs[i].id] = obj.runs[i];
	    }
	    var select = $("#run-to-view");
	    var selected = select.val();
	    var lastid = 0;
	    select.empty();
	    if (obj.runs.length > 0) {
		for (var i in this.runs) {
		    var run = this.runs[i];
		    $("<option>").attr("value",run.id).data("subtext",run.language)
			.text("Run " + run.number).appendTo(select).
			data("icon",run.is_a_test?"glyphicon-flag":
			     (run.has_been_run?"glyphicon-check":""));
		    lastid = run.id;
		}
		if (obj.echo !== undefined && obj.echo.run !== undefined) {
		    selected = obj.echo.run;
		}
		select.val(selected);
		if (select.val() != selected) {
		    select.val(lastid);
		}
		setTimeout(this._select_run,0);
	    } else {
		$(".disable-until-run").show();
	    }
	    select.selectpicker("refresh");
	}	
	if (obj.upload !== undefined) {
	    $.growl({
		title: "<strong>Upload Complete</strong>",
		message: "Your new code was uploaded successfully, as Run " +
		    obj.upload.number + ". A run has been scheduled.",
		icon: "glyphicon glyphicon-send"
	    }, {
		type: "info",
		delay: 4000,
	    });
	    $("#run-to-view").val(obj.upload.id).selectpicker("refresh");
	    this._select_run();
	}
	if (obj.notify) {
	    var growl = $.growl({
		title: obj.notif_title,
		message: obj.notify,
		icon: "glyphicon glyphicon-" + (obj.icon || "send"),
		url: obj.link
	    }, {
		type: obj.notif_type || "success",
		delay: obj.link ? 8000 : 4000
	    });
	    if (obj.link) {
		growl.$template.click(( function(){this.close()} ).bind(growl))
	    }
	}
    },
    _ws_open: function onopen(e) {
	$("#websocket-overlay-text").text("Connection Successful!");
	$("#websocket-overlay-icon").removeClass("glyphicon-signal").addClass("glyphicon-globe");
	setTimeout(function(){$("#websocket-overlay").modal("hide");},500);
	this._ws_delay = 500;
	this.send({competition: this.cid, mode: this.mode});
	this._load_problem();
	window.addEventListener("hashchange",this._load_problem);
    },
    _ws_close: function onclose(e) {
	$("#websocket-overlay-text").html("Lost Connection to Server!");
	$("#websocket-overlay-icon").removeClass("glyphicon-signal glyphicon-globe")
	    .addClass("glyphicon-exclamation-sign");
	this._ws_delay *= 2;
	this._ws_reconnect_delay = this._ws_delay;
	this._ws_reconnect_time();
	setTimeout(this._create_ws,this._ws_delay);
    },
    _ws_reconnect_time: function reconnect_time() {
	$("#websocket-overlay-reconnect").text("Will attempt to reconnect in " +
						      (this._ws_reconnect_delay/1000) +
						      " seconds.");
	if (this._ws_reconnect_delay > 0) {
	    this._ws_reconnect_delay -= 1000;
	    setTimeout(this._ws_reconnect_time,1000);
	} else {
	    $("#websocket-overlay-reconnect").text("");
	}
    },
    _ws_handlers: [ "open", "close", "message" ],
    _ws_delay: 500,
}

Mercury.initApp("Competition",CompetitionApp);
