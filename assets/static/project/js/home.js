function addLedClass(objectId, ledClass) {
	var obj = document.getElementById(objectId);
	if (!obj) {console.error(objectId + " not found");
		return;
	}
	obj.classList.remove("led-green");
	obj.classList.remove("led-green-on");
	obj.classList.remove("led-green-off");
	obj.classList.remove("led-red");
	obj.classList.remove("led-red-on");
	obj.classList.remove("led-red-off");
	obj.classList.remove("led-blue");
	obj.classList.remove("led-blue-on");
	obj.classList.remove("led-blue-off");
	obj.classList.add(ledClass);
}

function removeClass(objectId, className) {
	var obj = document.getElementById(objectId);
	if (!obj) {console.error(objectId + " not found");
		return;
	}
	obj.classList.remove(className);
}

function addClass(objectId, className) {
	var obj = document.getElementById(objectId);
	if (!obj) {console.error(objectId + " not found");
		return;
	}
	obj.classList.add(className);
}

function addRelayNotify(objectId, message) {
	var obj = document.getElementById(objectId);
	if (!obj) {console.error(objectId + " not found");
		return;
	}
	obj.innerHTML = message;
	obj.style.visibility="visible";
}

function removeRelayNotify(objectId) {
	var obj = document.getElementById(objectId);
	if (!obj) {console.error(objectId + " not found");
		return;
	}
	obj.innerHTML = "";
	obj.style.display="hidden";
}

function _refreshHomeRelay(objectId, value, value_forced, debug=false) {
	var notifyObjectId = objectId + "_notify";
	if (!document.getElementById(objectId))
	{
		console.warn("_refreshHomeRelay", objectId + " not found");
		return;
	}
	if (value == "DISABLED" || value == "D" || value == "-") {
		if (debug) {console.log(objectId + " DISABLED");}
		addRelayNotify(notifyObjectId, gettext("Relé DESACTIVADO"));
		return;
	}
	if (value_forced == "1") {
		if (debug) {console.log(objectId + " FORCED ON");}
		addRelayNotify(notifyObjectId, gettext("FORZADO ON"));
		addLedClass(objectId, 'led-blue-on');
	}
	else if (value_forced == "2") {
		if (debug) {console.log(objectId + " FORCED OFF");}
		addRelayNotify(notifyObjectId, gettext("FORZADO OFF"));
		addLedClass(objectId, 'led-red-on');
	}
	else {
		removeRelayNotify(notifyObjectId);
		if (debug) {console.log(objectId + " value="+value);}
		if (value == "1")
			addLedClass(objectId, 'led-blue-on');
		else
			addLedClass(objectId, 'led-blue-off');
	}
}

function append_symbol_grade(value) {
	if (value != "-") value = value + "º";
	return value
}

function setHtmlToDiv(obj_name, html_text) {
	var obj = document.getElementById(obj_name);
	if (!obj) {
		console.warn("object name '" + obj_name + "' not found in Home page");
		return;
	}
	obj.innerHTML = html_text;
}

function setHomeCardValues(var_gauge, fieldname, value, value_min, value_max, append_to_value = "") {
	var obj_card_header = document.getElementById("card-header_" + fieldname);
	if (!obj_card_header) {
		console.error("object id 'card-header_" + fieldname + "' not found in Home page");
		return;
	}
	var obj_card_body = document.getElementById("card-body_" + fieldname);
	if (!obj_card_body) {
		console.error("object id 'card-body_" + fieldname + "' not found in Home page");
		return;
	}
	obj_card_header.style.backgroundColor="";
	if (value == "ERROR" || value == "E")
	{
		obj_card_header.style.backgroundColor="red";
		obj_card_body.style.visibility="hidden";
		setHtmlToDiv(fieldname + '_value', gettext("Sonda ERROR"));
		return;
	}
	else if (value == "DISABLED" || value == "D" || value == "-")
	{
		obj_card_header.style.backgroundColor="gray";
		obj_card_body.style.visibility="hidden";
		setHtmlToDiv(fieldname + '_value', gettext("Sonda DESACTIVADA"));
		return;
	}
	else {
		obj_card_header.style.backgroundColor="black";
		obj_card_body.style.visibility="visible";
	}

	value_grade = append_symbol_grade(value);
	setHtmlToDiv(fieldname + '_value', " (" + value_grade + ")");

	if (append_to_value) {
		setHtmlToDiv(fieldname + '_append_to_value', " " + append_to_value);
	} else {
		setHtmlToDiv(fieldname + '_append_to_value', "");
	}

	value_grade = append_symbol_grade(value_min);
	setHtmlToDiv(fieldname + '_min', value_grade);

	value_grade = append_symbol_grade(value_max);
	setHtmlToDiv(fieldname + '_max', value_grade);

	if (var_gauge)
	{
		var temperatura = parseFloat(value);
		var_gauge.series[0].points[0].update(temperatura);
	}
}

function setHomeValueIp(ip_local, ip_public) {
	if (ip_local || ip_public) {
		let html = "<i class='fa-solid fa-laptop'></i>&nbsp;";
		if (ip_local) {
			html += "<a target='_blank' href='http://" + ip_local + "' style='color:white;'>" +
					ip_local + "</a>";
		}
		if (ip_public) {
			html += "&nbsp;&nbsp;<i class='fa-solid fa-globe'></i>&nbsp;" + ip_public;
		}
		setHtmlToDiv('data_ip', html);
	}
}

function setHomeValueUpdated(value) {
	if (document.getElementById("float-info-div-time-span") && value) {
		setHtmlToDiv('data_updated_at', "<i class='fa-regular fa-clock'></i>&nbsp;" + value);
	}
}

function setHomeValueTempColector1(value, value_min, value_max, append_to_value) {
	if (typeof gauge_data_temp_calle !== 'undefined' && gauge_data_temp_calle !== null) {
		setHomeCardValues(gauge_data_temp_calle, "data_temp_calle", value, value_min, value_max, append_to_value);
	}
	else {
		console.warn("setHomeValueTempColector1", "gauge_data_temp_calle variable not found");
	}
}

function setHomeValueTempDepUp(value, value_min, value_max) {
	if (typeof gauge_data_temp_depup !== 'undefined' && gauge_data_temp_depup !== null) {
		setHomeCardValues(gauge_data_temp_depup, "data_temp_depup", value, value_min, value_max);
	}
	else {
		console.warn("setHomeValueTempDepUp", "gauge_data_temp_depup variable not found");
	}
}

function setHomeValueTempDepDown(value, value_min, value_max) {
	if (typeof gauge_data_temp_depdown !== 'undefined' && gauge_data_temp_depdown !== null) {
		setHomeCardValues(gauge_data_temp_depdown, "data_temp_depdown", value, value_min, value_max);
	}
	else {
		console.warn("setHomeValueTempDepDown", "gauge_data_temp_depdown variable not found");
	}
}

function setHomeValueTempAir(value, value_min, value_max) {
	if (typeof gauge_data_temp_air !== 'undefined' && gauge_data_temp_air !== null) {
		setHomeCardValues(gauge_data_temp_air, "data_temp_air", value, value_min, value_max);
	}
	else {
		console.warn("setHomeValueTempAir", "gauge_data_temp_air variable not found");
	}
}

function setHomeValueRelayErrors(relay_value, relay_value_forced) {
	_refreshHomeRelay("data_relay_errors", relay_value, relay_value_forced);
}

function setHomeValueRelayPump1(relay_value, relay_value_forced) {
	_refreshHomeRelay("data_relay_pump1", relay_value, relay_value_forced);
}

function setHomeValueRelayPump2(relay_value, relay_value_forced) {
	_refreshHomeRelay("data_relay_pump2", relay_value, relay_value_forced);
}

function setHomeValueRelayPump3(relay_value, relay_value_forced) {
	_refreshHomeRelay("data_relay_pump3", relay_value, relay_value_forced);
}

function setHomeValueRelayColector1Higher(relay_value, relay_value_forced) {
	_refreshHomeRelay("data_relay_colector1_higher", relay_value, relay_value_forced);
}

function setHomeValueRelayColector1Lower(relay_value, relay_value_forced) {
	_refreshHomeRelay("data_relay_colector1_lower", relay_value, relay_value_forced);
}

function setHomeValueRelayColector2Higher(relay_value, relay_value_forced) {
	_refreshHomeRelay("data_relay_colector2_higher", relay_value, relay_value_forced);
}

function setHomeValueRelayColector2Lower(relay_value, relay_value_forced) {
	_refreshHomeRelay("data_relay_colector2_lower", relay_value, relay_value_forced);
}

function setHomeValueRelayColector3Higher(relay_value, relay_value_forced) {
	_refreshHomeRelay("data_relay_colector3_higher", relay_value, relay_value_forced);
}

function setHomeValueRelayColector3Lower(relay_value, relay_value_forced) {
	_refreshHomeRelay("data_relay_colector3_lower", relay_value, relay_value_forced);
}

function setHomeValueRelayDepupHigher(relay_value, relay_value_forced) {
	_refreshHomeRelay("data_relay_depup_higher", relay_value, relay_value_forced);
}

function setHomeValueRelayDepupLower(relay_value, relay_value_forced) {
	_refreshHomeRelay("data_relay_depup_lower", relay_value, relay_value_forced);
}

function setHomeValueRelayDepdownHigher(relay_value, relay_value_forced) {
	_refreshHomeRelay("data_relay_depdown_higher", relay_value, relay_value_forced);
}

function setHomeValueRelayDepdownLower(relay_value, relay_value_forced) {
	_refreshHomeRelay("data_relay_depdown_lower", relay_value, relay_value_forced);
}
