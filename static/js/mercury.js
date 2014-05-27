
function MercuryApplication() {
    var src = $("script[data-static-js]").attr("src");
    this.static_path = src.substring(0,src.lastIndexOf("/js/")) + "/";

    this.apps = [];
    this._appQueue = [];
    this._initialized = false;

    for (i in this[name]) {
	    if (typeof this[name][i] == "function") {
		this[name][i] = this[name][i].bind(this[name]);
	    }
	}
};

MercuryApplication.prototype = {
    initApp: function newApp(name,constructor) {
	if (this._initialized) {
	    this._loadApp(name,constructor);
	} else {
	    this._appQueue.push([name,constructor]);
	}
    },
    _loadApp: function loadApp(name,constructor) {
	this[name] = this[name] || (constructor?(new constructor()):{});
	this.apps.push(name);
	for (i in this[name]) {
	    if (typeof this[name][i] == "function") {
		this[name][i] = this[name][i].bind(this[name]);
	    }
	}
	if (this[name].onload) { this[name].onload() };
    },
    _loadQueued: function loadQueued() {
	for (i in this._appQueue) {
	    this._loadApp(this._appQueue[i][0],this._appQueue[i][1]);
	}
	this._initialized = true;
    },


    /** Helper funcs **/
    getAlertMarkup: function alertBefore(msg,type) {
	type = type?type:"danger";
	return '<div class="alert alert-{} alert-dismissable">\
  <button type="button" class="close" data-dismiss="alert">&times;</button>\
  {}</div>'.format(type,msg);
    }
};

function ModalApp() {
    this._dialogIsOpen = false;
};

ModalApp.prototype = {
    _showModal: function showModal(markup,callbacks) {
	if (this._dialogIsOpen) {
	    setTimeout(this._showModal.bind(this,markup,callbacks),100);
	    return false;
	}
	$("body").append(markup);
	this._dialogIsOpen = true;
	var modal = $(".mercury-modal-app-root").modal()
	    .on("hidden.bs.modal", this._onHidden)
	    .on("hide.bs.modal", callbacks["cancel"])
	    .find(".btn-primary").click(callbacks["okay"]);
    },
    alert: function alert(msg,title,button) {
	var markup = this.dialogMarkup.format({ body: msg, title: this._getTitle(),
						footer: this.cancelMarkup.format({
						    cancel: this._stringOnly(button,"Okay")})
					      });
	this._showModal(markup,{cancel: this._closeCallback.bind(this,this._getCallback(),
								 null)});
    },
    confirm: function confirm(msg,title,yes,no) {
	var markup = this.dialogMarkup.format({ body: msg, title: this._getTitle(),
						footer: this.cancelMarkup.format({
						    cancel: this._stringOnly(no,"No")}) +
						this.okayMarkup.format({
						    okay: this._stringOnly(yes,"Yes")}) });
	this._showModal(markup,{cancel: this._closeCallback.bind(this,this._getCallback(),
								 false),
				okay: this._closeCallback.bind(this,this._getCallback(),
							       true)});
    },
    prompt: function prompt(msg,title,value,okay,cancel) {
	throw new TypeError("prompt is not implemented yet");
    },
    _onHidden: function onHidden(e) {
	$(".mercury-modal-app-root").remove();
	this._dialogIsOpen = false;
    },
    _closeCallback: function alertCallback(callback,okay) {
	if (okay) {
	    $(".mercury-modal-app-root").off("hide.bs.modal"); }
	callback(okay);
    },
    _stringOnly: function (arg,fallback) {
	return (arg && typeof arg == "string")?arg:fallback;
    },
    _getCallback: function getCallback(args) {
	var args = args || arguments.callee.caller.arguments;
	for (i in args) {
	    if (typeof args[i] == "function") {
		return args[i];
	    }
	}
	return (function(){});
    },
    _getTitle: function getTitle(args) {
	var args = args || arguments.callee.caller.arguments;
	return (args[1] && typeof args[1] == "string")?args[1]:args[0];
    },
    dialogMarkup: '<div class="modal fade mercury-modal-app-root" tabindex="-1" role="dialog">\
  <div class="modal-dialog">\
    <div class="modal-content">\
      <div class="modal-header">\
        <button type="button" class="close" data-dismiss="modal">&times;</button>\
        <h3 class="modal-title">{title}</h3>\
      </div>\
      <div class="modal-body">{body}</div>\
      <div class="modal-footer">{footer}</div>\
    </div>\
  </div>\
</div>',
    promptMarkup: '<input type="text" class="mercury-modal-app-prompt" value="{value}"/>',
    cancelMarkup: '<button type="button" class="btn btn-default" data-dismiss="modal">{cancel}</button>',
    okayMarkup: '<button type="button" class="btn btn-primary" data-dismiss="modal">{okay}</button>'
};

var Mercury = window.Mercury || new MercuryApplication();

$(Mercury._loadQueued.bind(Mercury));

Mercury.initApp("Modal",ModalApp);
