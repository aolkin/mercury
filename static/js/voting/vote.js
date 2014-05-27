
function VotingApp() {};

VotingApp.prototype = {
    onload: function onload() {
	this.questions = {};
	this.choices = {};
	$(".irv-container button").click(this.setRank).each(this._getQuestions);
	$(".irv-container .irv-text").each(this._getChoices);
	$(".voting-submit").click(this.submit);
    },
    setRank: function setRank(e) {
	var el = $(e.target);
	el.siblings(".btn-primary").removeClass("btn-primary").addClass("btn-default");
	$("button[data-question="+el.data("question")+"][data-number="+el.data("number")+"]")
	    .removeClass("btn-primary").addClass("btn-default");
	el.removeClass("btn-default").addClass("btn-primary");
	this.questions[el.data("question")][el.data("number")] = el.data("choice");
    },
    _getQuestions: function getQuestions(index,el) {
	this.questions[$(el).data("question")] = {1: null, 2: null, 3: null};
    },
    _getChoices: function getChoices(index,el) {
	this.choices[$(el).siblings(".irv-choices").children("[data-choice]")
		     .data("choice")] = $(el).text();
    },
    submit: function submit() {
	$(".irv-container .alert").remove();
	var names = {};
	for (i in this.questions) {
	    names[i] = {};
	    for (j in this.questions[i]) {
		if (this.questions[i][j]) {
		    names[i][j] = this.choices[this.questions[i][j]];
		} else {
		    $("div[data-question="+i+"] h4").before(
			Mercury.getAlertMarkup("<strong>Incomplete Question:</strong> " +
					       "Please select three choices!"));
		    $.scrollTo($("div[data-question="+i+"]").parents(".panel"),200);
		    return false;
		}
	    }
	}
	markup = "<ul>";
	for (i in names) {
	    markup += ("<li><strong>{}</strong><ol><li>{}</li><li>{}</li>" +
		       "<li>{}</li></ol></li>").format(
			   $("h4[data-question="+i+"]").text(),
			   names[i][1],names[i][2],names[i][3]);
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
