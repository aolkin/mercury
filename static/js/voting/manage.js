
function ResultsApp() {}

ResultsApp.prototype = {
    onload: function onload() {
	this.loadResults();
	$(".reload-results").click(this.loadResults);
	$(".show-result-steps").click(this.showResultSteps);
    },
    loadResults: function loadResults() {
	$(".results-body").append(this.loadingHTML);
	$.getJSON("results",this.processResults);
    },
    processResults: function processResults(data,status,xhr) {
	console.log(data);
	$(".results-body").empty();
	var root = $("<ul>").appendTo($(".results-body"));
	for (i in data) {
	    var el = $("<li>").appendTo(root);
	    $("<span>").appendTo(el).text(i + ": " + data[i][0]);
	    var steps = data[i][1];
	    var steplist = $("<ol>").addClass("hide result-step-list").appendTo(el);
	    for (s in steps) {
		var step = $("<li>").appendTo(steplist);
		var list = $("<ul>").appendTo(step);
		var choices = steps[s][0];
		for (c in choices) {
		    $("<li>").appendTo(list).text(c + ": " + choices[c]);
		}
		$("<span>").appendTo(step).addClass("results-step-worst").text(JSON.stringify(steps[s][1]));
	    }
	}
    },
    showResultSteps: function showResultSteps() {
	$(".result-step-list").toggleClass("hide");
    },
    loadingHTML: '<div class="loading">\
      <img class="center-block " width="32" height="32" src="' + Mercury.static_path +
	'images/loading-circle.gif" />\
      <p class="lead text-center">Loading results...</div>\
    </div>'
}

Mercury.initApp("VotingResults",ResultsApp);
