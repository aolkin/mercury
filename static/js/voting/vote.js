
function VotingApp() {};

VotingApp.prototype = {
    onload: function onload() {
	this.questions = {};
	this.choices = {};
	$(".irv-container,.stv-container button").click(this.setRank).each(this._getQuestions);
	$(".irv-container,.stv-container .irv-text,.stv-text").each(this._getChoices);

    $('.hw-container button').click(this.chooseHW).each(this._getHWQuestions);
    $('.hw-container .hw-text').each(this._getChoices);

    $(".voting-submit").click(this.submit);
    },
    setRank: function setRank(e) {
	var el = $(e.target);
	var question = this.questions[el.data("question")];
	for (q in question) {
	    if (question[q] == el.data("choice")) {
		question[q] = false;
	    }
	}
	el.siblings(".btn-primary").removeClass("btn-primary").addClass("btn-default");
	$("button[data-question="+el.data("question")+"][data-number="+el.data("number")+"]")
	    .removeClass("btn-primary").addClass("btn-default");
	el.removeClass("btn-default").addClass("btn-primary");
	question[el.data("number")] = el.data("choice");
    },
    chooseHW: function chooseHW(e) {
    	var el = $(e.target);
    	var question = this.questions[el.data('question')];
        if (!(question instanceof Array)) {
            var old = question;
            question = Array();
            this.questions[el.data('question')] = question;
            for (var i in old) {
                question.push(old[i]);
            }
        }
        var index = question.indexOf(el.data('choice'));
        if (index != -1) {
            el.removeClass('btn-primary').addClass('btn-default');
            question.splice(index, 1);
        } else {
            if (question.length >= 3) {
                question.splice(0);
                $('.hw-container button.btn-primary').removeClass('btn-primary').addClass('btn-default');
            }
            question.push(el.data('choice'));
            el.removeClass('btn-default').addClass('btn-primary');
        }
    },
    _getQuestions: function getQuestions(index,el) {
	this.questions[$(el).data("question")] = {0: null, 1: null, 2: null};
    },
    _getHWQuestions: function getHWQuestions(index, el) {
	    this.questions[$(el).data("question")] = Array();
    },
    _getChoices: function getChoices(index,el) {
	this.choices[$(el).siblings(".irv-choices,.stv-choices,.hw-choices").children("[data-choice]")
		     .data("choice")] = $(el).text();
    },
    submit: function submit() {
	$(".irv-container,.stv-container,.hw-container .alert").remove();
	var names = {};
	for (i in this.questions) {
	    names[i] = {};
        var curr = this.questions[i];
        if (curr instanceof Array) {
            if (curr.length < 3) {
                $("div[data-question="+i+"] h4").before(
    			Mercury.getAlertMarkup("<strong>Incomplete Question:</strong> " +
    					       "Please select three choices!"));
    		    $.scrollTo($("div[data-question="+i+"]").parents(".panel"), 200);
    		    return false;
            }
            this.questions[i] = {0: curr[0], 1: curr[1], 2: curr[2]};
        }
	    for (j in this.questions[i]) {
		if (this.questions[i][j]) {
		    names[i][j] = this.choices[this.questions[i][j]];
		} else {
		    /*$("div[data-question="+i+"] h4").before(
			Mercury.getAlertMarkup("<strong>Incomplete Question:</strong> " +
					       "Please select three choices!"));
		    $.scrollTo($("div[data-question="+i+"]").parents(".panel"),200);
		    return false;*/
		}
	    }
	}
	markup = "<ul>";
	for (i in names) {
	    markup += ("<li><strong>{}</strong><ol><li>{}</li><li>{}</li>" +
		       "<li>{}</li></ol></li>").format(
			   $("h4[data-question="+i+"]").text(),
			   names[i][0] || "No Selection",
			   names[i][1] || "No Selection",
			   names[i][2] || "No Selection");
	}
	markup += "</ul>"+'<div class="alert alert-danger">{}</div>'.format(
	    "After submitting, You will not be able to change your selections.");
	Mercury.Modal.confirm(markup,"Submit These Selections?",this._sendData);
    },
    _sendData: function sendData(okay) {
	if (!okay) { return false; }
	$.post("","data="+JSON.stringify(this.questions),null,"json")
	    .always((function(data,status,xhr){
		if (status !== "success")  {
		    Mercury.Modal.alert(this._errorMarkup.format(data.statusText + " (" +
								 xhr + ")"),"Error!");
		    return false;
		}
		if (!data.success)  {
		    Mercury.Modal.alert(this._errorMarkup.format(data.error?data.error:
								 "Unknown Error"),"Error!");
		    return false;
		}
		location.assign(data.redirect);
	    }).bind(this));
    },
    _errorMarkup: '<p><big class="text-danger">Error submitting your choices:</big></p>\
<p class="text-danger well well-sm">{}</p>'
}

Mercury.initApp("Voting",VotingApp);
