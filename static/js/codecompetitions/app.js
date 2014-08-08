
function CompetitionApp() {
    this.mode = mode;
    this.cid = cid;
    this.runs = [];
    this.run = null;
};

CompetitionApp.prototype = {
    onload: function onload() {
	this._create_ws();
	$("#run-to-view").change(this._select_run);
	$("#source-to-view").change(this._select_source);
	if (this.mode !== "compete") {
	    $("#player-to-judge").change(this._select_player);
	}
    },
    _load_problem: function load_problem() {
	var parts = location.hash.substr(1).split("-",2);
	var pid = parts[0], problem = parts[1];
	if (pid) {
	    $(".problem-name").text(decodeURIComponent(problem));
	    $(".problem-description").text("Loading...");
	    $("a.problem-"+pid).parent().addClass("active").siblings().removeClass("active");
	    this.send({"problem":parseInt(pid)});
	}
    },
    _select_run: function select_run() {
	$(".disable-until-run").hide();
	var run = this.runs[$("#run-to-view").val()];
	this.run = run;
	console.log(run);
	$(".run-output").text(run.output);
	$(".compile-failure").text(run.compiled_successfully?"":"Compilation Failure");
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
    _select_player: function select_player() {
	this.send({player:$("#player-to-judge").val()});
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
	
	if (obj.description !== undefined) {
	    $(".disable-until-problem").hide();
	    $(".problem-description").html(obj.description);
	}
	if (obj.expected_output !== undefined) {
	    $(".expected-output").text(obj.expected_output);
	}
	if (obj.running !== undefined) {
	    $("#contest-state").text(obj.running?"Running":"Stopped");
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
	    this._select_player();
	}
	if (obj.runs) {
	    this.runs = {};
	    for (i in obj.runs) {
		this.runs[obj.runs[i].id] = obj.runs[i];
	    }
	    var select = $("#run-to-view");
	    var selected = select.val();
	    select.empty();
	    if (obj.runs.length > 0) {
		for (var i in this.runs) {
		    var run = this.runs[i];
		    $("<option>").attr("value",run.id).data("subtext",run.language)
			.text("Run " + run.number).appendTo(select).
			data("icon",run.is_a_test?"glyphicon-flag":
			     (run.has_been_run?"glyphicon-check":""));
		}
		select.val(selected);
		setTimeout(this._select_run,0);
	    } else {
		$(".disable-until-run").show();
	    }
	    select.selectpicker("refresh");
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
