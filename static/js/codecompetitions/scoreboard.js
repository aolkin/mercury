
function ScoreboardApp() {
    this.cid = cid;
};

ScoreboardApp.prototype = {
    onload: function onload() {
	this._create_ws();
	if (window.opener) { $("#close-popup").click(function(){ window.close(); }); }
	if ($("#start-timer").length) {
	    $("#start-timer").click(this._start_timer);
	    $("#stop-timer").click(this._stop_timer);
	}
    },
    _create_ws: function createWS() {
	$("#websocket-overlay").modal("show");
	$("#websocket-overlay-text").text("Connecting...");
	$("#websocket-overlay-icon").removeClass("glyphicon-dashboard")
	    .addClass("glyphicon-signal");
	this.ws = new WebSocket(wsaddress + "scoreboard/");
	for (i in this._ws_handlers) {
	    this.ws["on"+this._ws_handlers[i]] = this["_ws_"+this._ws_handlers[i]];
	}
    },
    _start_timer: function start_timer() {
	this.send({clock:"start"});
    },
    _stop_timer: function stop_timer() {
	this.send({clock:"stop"});
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

	if (obj.scores) {
	    var t = $("#main-board").empty();
	    var cols = t.siblings("thead").find("th").length;
	    for (var i = 0; i < obj.scores.length; i++) {
		var tr = $("<tr>").appendTo(t);
		tr.append($("<td>").text(i+1));
		tr.append($("<td>").text(obj.scores[i].player));
		tr.append($("<td>").text(obj.scores[i].total_score));
		tr.append($("<td>").text(obj.scores[i].average_score));
		var p_index = 0;
		for (var p in obj.scores[i].problems) {
		    while (p > p_index) {
			tr.append($("<td>").text("N/A").addClass("text-muted"));
			p_index += 1;
		    }
		    tr.append($("<td>").text(obj.scores[i].problems[p].score));
		    p_index += 1;
		}
		while (cols - 4 > p_index) {
		    tr.append($("<td>").text("N/A").addClass("text-muted"));
		    p_index += 1;
		}
	    }
	}

	if (obj.running !== undefined) {
	    $("#contest-state").html(obj.running?"Running":"Stopped");
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
    },
    _ws_open: function onopen(e) {
	$("#websocket-overlay-text").text("Connection Successful!");
	$("#websocket-overlay-icon").removeClass("glyphicon-signal")
	    .addClass("glyphicon-globe");
	setTimeout(function(){$("#websocket-overlay").modal("hide");},500);
	this._ws_delay = 500;
	this.send({competition: this.cid });
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
};

Mercury.initApp("Scoreboard",ScoreboardApp);
