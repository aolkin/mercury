/**
 * Copyright (c) 2007-2014 Ariel Flesler - aflesler<a>gmail<d>com | http://flesler.blogspot.com
 * Licensed under MIT
 * @author Ariel Flesler
 * @version 1.4.12
 */
(function(a){if(typeof define==='function'&&define.amd){define(['jquery'],a)}else{a(jQuery)}}(function($){var j=$.scrollTo=function(a,b,c){return $(window).scrollTo(a,b,c)};j.defaults={axis:'xy',duration:parseFloat($.fn.jquery)>=1.3?0:1,limit:true};j.window=function(a){return $(window)._scrollable()};$.fn._scrollable=function(){return this.map(function(){var a=this,isWin=!a.nodeName||$.inArray(a.nodeName.toLowerCase(),['iframe','#document','html','body'])!=-1;if(!isWin)return a;var b=(a.contentWindow||a).document||a.ownerDocument||a;return/webkit/i.test(navigator.userAgent)||b.compatMode=='BackCompat'?b.body:b.documentElement})};$.fn.scrollTo=function(f,g,h){if(typeof g=='object'){h=g;g=0}if(typeof h=='function')h={onAfter:h};if(f=='max')f=9e9;h=$.extend({},j.defaults,h);g=g||h.duration;h.queue=h.queue&&h.axis.length>1;if(h.queue)g/=2;h.offset=both(h.offset);h.over=both(h.over);return this._scrollable().each(function(){if(f==null)return;var d=this,$elem=$(d),targ=f,toff,attr={},win=$elem.is('html,body');switch(typeof targ){case'number':case'string':if(/^([+-]=?)?\d+(\.\d+)?(px|%)?$/.test(targ)){targ=both(targ);break}targ=win?$(targ):$(targ,this);if(!targ.length)return;case'object':if(targ.is||targ.style)toff=(targ=$(targ)).offset()}var e=$.isFunction(h.offset)&&h.offset(d,targ)||h.offset;$.each(h.axis.split(''),function(i,a){var b=a=='x'?'Left':'Top',pos=b.toLowerCase(),key='scroll'+b,old=d[key],max=j.max(d,a);if(toff){attr[key]=toff[pos]+(win?0:old-$elem.offset()[pos]);if(h.margin){attr[key]-=parseInt(targ.css('margin'+b))||0;attr[key]-=parseInt(targ.css('border'+b+'Width'))||0}attr[key]+=e[pos]||0;if(h.over[pos])attr[key]+=targ[a=='x'?'width':'height']()*h.over[pos]}else{var c=targ[pos];attr[key]=c.slice&&c.slice(-1)=='%'?parseFloat(c)/100*max:c}if(h.limit&&/^\d+$/.test(attr[key]))attr[key]=attr[key]<=0?0:Math.min(attr[key],max);if(!i&&h.queue){if(old!=attr[key])animate(h.onAfterFirst);delete attr[key]}});animate(h.onAfter);function animate(a){$elem.animate(attr,g,h.easing,a&&function(){a.call(this,targ,h)})}}).end()};j.max=function(a,b){var c=b=='x'?'Width':'Height',scroll='scroll'+c;if(!$(a).is('html,body'))return a[scroll]-$(a)[c.toLowerCase()]();var d='client'+c,html=a.ownerDocument.documentElement,body=a.ownerDocument.body;return Math.max(html[scroll],body[scroll])-Math.min(html[d],body[d])};function both(a){return $.isFunction(a)||typeof a=='object'?a:{top:a,left:a}};return j}));

/*! Bootstrap Growl - v1.0.6 - 2014-01-29
* https://github.com/mouse0270/bootstrap-growl
* Copyright (c) 2014 Remable Designs; Licensed MIT */
!function(a){"use strict";var b=[];a.growl=function(c,d){var e,f,g,h,i=null,j=null,k=null;switch("[object Object]"==Object.prototype.toString.call(c)?(i=c.message,j=c.title?" "+c.title+" ":null,k=c.icon?c.icon:null):i=c,d=a.extend(!0,{},a.growl.default_options,d),d.template.icon="class"===d.template.icon_type?'<span class="">':'<img src="" />',f="bootstrap-growl-"+d.position.from+"-"+d.position.align,e=a(d.template.container),e.addClass(f),e.addClass(d.type?"alert-"+d.type:"alert-info"),d.allow_dismiss&&e.append(a(d.template.dismiss)),k&&e.append(d.template.icon?"class"==d.template.icon_type?a(d.template.icon).addClass(k):a(d.template.icon).attr("src",k):k),j&&(e.append(d.template.title?a(d.template.title).html(j):j),e.append(d.template.title_divider)),e.append(d.template.message?a(d.template.message).html(i):i),h=d.offset,a("."+f).each(function(){return h=Math.max(h,parseInt(a(this).css(d.position.from))+a(this).outerHeight()+d.spacing)}),g={position:"body"===d.ele?"fixed":"absolute",margin:0,"z-index":d.z_index,display:"none"},g[d.position.from]=h+"px",e.css(g),a(d.ele).append(e),d.position.align){case"center":e.css({left:"50%",marginLeft:-(e.outerWidth()/2)+"px"});break;case"left":e.css("left",d.offset+"px");break;case"right":e.css("right",d.offset+"px")}d.onGrowlShow&&d.onGrowlShow(event);e.fadeIn(d.fade_in,function(a){d.onGrowlShown&&d.onGrowlShown(a),d.delay>0&&(1==d.pause_on_mouseover&&e.on("mouseover",function(){clearTimeout(b[e.index()])}).on("mouseleave",function(){b[e.index()]=setTimeout(function(){return e.alert("close")},d.delay)}),b[e.index()]=setTimeout(function(){return e.alert("close")},d.delay))});return e.bind("close.bs.alert",function(a){d.onGrowlClose&&d.onGrowlClose(a)}),e.bind("closed.bs.alert",function(b){d.onGrowlClosed&&d.onGrowlClosed(b);var c=a(this).css(d.position.from);a(this).nextAll("."+f).each(function(){a(this).css(d.position.from,c),c=parseInt(c)+d.spacing+a(this).outerHeight()})}),e},a.growl.default_options={ele:"body",type:"info",allow_dismiss:!0,position:{from:"top",align:"right"},offset:20,spacing:10,z_index:1031,fade_in:400,delay:5e3,pause_on_mouseover:!1,onGrowlShow:null,onGrowlShown:null,onGrowlClose:null,onGrowlClosed:null,template:{icon_type:"class",container:'<div class="col-xs-10 col-sm-10 col-md-3 alert">',dismiss:'<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>',title:"<strong>",title_divider:"",message:""}}}(jQuery,window,document);

String.prototype.format = function() {
    var args = arguments;
    this.unkeyed_index = 0;
    return this.replace(/\{(\w*)\}/g, function(match, key) { 
        if (key === '') {
            key = this.unkeyed_index;
            this.unkeyed_index++
        }
        if (key == +key) {
            return args[key] !== 'undefined'
                ? args[key]
                : match;
        } else {
            for (var i = 0; i < args.length; i++) {
                if (typeof args[i] === 'object' && typeof args[i][key] !== 'undefined') {
                    return args[i][key];
                }
            }
            return match;
        }
    }.bind(this));
};

$(function(){$(".selectpicker").selectpicker({"mobile":true,"showSubtext":true});});
