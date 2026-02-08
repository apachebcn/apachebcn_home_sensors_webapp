function loading_get() {
	return document.getElementById('loading');
}

function loading_on() {
	const loading = loading_get();
	if(!loading) return;
	loading.style.display = "flex";  // aquí usamos flex al mostrar
}

function loading_off() {
	const loading = loading_get();
	if(!loading) return;
	loading.style.display = "none";
}

function pausa(millis)
{
	var date = new Date();
	var curDate = null;
	do { curDate = new Date(); }
	while(curDate-date < millis);
}

function enviar_seleccion_usuario(user_id) {
	showDialogModMsg("Reload", "Changing user");
	$.ajax({
		type: "GET",
		url: '/change_profile_user_selected/' + user_id,
		success: function(data)
		{
			pausa(1000)
			document.getElementById('sel_cliente').submit();
			//alert(data); // show response from the php script.
		}
	});
}

function showDialogMod () {
	var dialogmod = $('#DialogMod');
	dialogmod.modal('show');
}

function showDialogModMsg(MsgHead, MsgContent) {
	var dialogmod = $('#DialogMod');
	var modal_header = document.getElementById('modal-header');
	var dialog_head = document.getElementById('dialog_head');
	var dialog_content = document.getElementById('dialog_content');
	dialog_head.innerText = MsgHead;
	dialog_content.innerText = MsgContent;
	modal_header.style.backgroundColor = "blue";
	dialogmod.modal('show');
}

function showDialogModErrorMsg(MsgHead, MsgContent) {
	var dialogmod = $('#DialogMod');
	var modal_header = document.getElementById('modal-header');
	var dialog_head = document.getElementById('dialog_head');
	var dialog_content = document.getElementById('dialog_content');
	dialog_head.innerText = MsgHead;
	dialog_content.innerText = MsgContent;
	modal_header.style.backgroundColor = "red";
	dialogmod.modal('show');
}

function hideDialogMod () {
	// Agregar un retraso antes de ocultar el modal
	setTimeout(function() {
		hideDialogMod();
	}, 100); // Retraso de 1000 ms
	var dialogmod = $('#DialogMod');
	dialogmod.modal('hide');
}

function insert_onclick_alert_msg(msg) {
	if (msg == "") return "";
	msg = msg.replace(/<br\s*\/?>/gi, "\\n")   // convertir <br> a \n
			 .replace(/>\s*(\\n|$)/g, "$1")    // eliminar '>' al final de cada línea o string
			 .replace(/'/g, "\\'")
			 .replace(/"/g, '\\"');
	return `onclick="alert('${msg}')"`; 
}

function get_formated_float_info_cell(div_id, icon, value, tooltip_text, div_input_tags, innerHtml = "") {
	if (tooltip_text) {
		return `<div `+div_input_tags+` ${insert_onclick_alert_msg(tooltip_text)} id="`+div_id+`" class="float-info-div"><span id="`+div_id+`-span" class="float-info-span-head"><i class="` + icon + `" aria-hidden="true"></i> ` + value + `</span><div class="tooltip-text">` + tooltip_text + `</div>` +  innerHtml + `</div>`;
	}
	return `<div `+div_input_tags+` id="`+div_id+`" class="float-info-div"><span id="`+div_id+`-span" class="float-info-span-head"><i class="` + icon + `" aria-hidden="true"></i> ` + value + `</span>` +  innerHtml + `</div>`;
}

const safeParseFloat = (value) => {
	value = String(value).replace(",", ".");
	const num = parseFloat(value); // Solo necesita el valor
	if (isNaN(num)) {
		// console.error(`Error: "${value}" no es un número válido en ${name_var}`);
		return null; 
	}
	return num;
};

function get_formated_float_info_cell_for_temp(div_id, name_var, icon, icon2, value, value_before, tooltip_text, div_input_tags) {
	if (value === "-" || value === "DISABLED" || value === "D") {
		return `<div ${div_input_tags} ${insert_onclick_alert_msg(tooltip_text)} id="`+div_id+`" class="float-info-div"><span id="`+div_id+`-span" class="float-info-span-head" style='color:darkgray'><i class="${icon}" aria-hidden="true"></i> OFF</span><div class="tooltip-text">${tooltip_text}</div></div>`;
	}
	let number_style = ``;
	const value_num = safeParseFloat(value);
	const value_before_num = safeParseFloat(value_before);
	if (value == "ERROR" || value == "E") {
		number_style = `style='background:red;'`;
	}
	else if (value_num !== null && value_before_num !== null) {
		if (value_num > value_before_num) {
			number_style = `style='color:coral;border-color:coral;'`;
		}
		if (value_num < value_before_num) {
			number_style = `style='color:cyan;border-color:cyan;'`;
		}
	}
	var line = `<div ${div_input_tags} ${insert_onclick_alert_msg(tooltip_text)} class="float-info-div">`
	line += `<span ${number_style} id="`+div_id+`-span" class="float-info-span-head">`;
	line += `<i class="${icon}" aria-hidden="true"></i>`;
	if (icon2) line += `&nbsp;<i class="${icon2}" aria-hidden="true"></i>`;
	if (value == "ERROR" || value == "E") {
		line += ` ERROR`;
	}
	else if (value == "DISABLED" || value == "D") {
		line += ` DISABLED`;
	}
	else if (value_num !== null && value_before_num !== null) {
		line += ` ${value}º`;
		if (value_num > value_before_num) {
			line += ` <i class="fa fa-arrow-up"></i>`;
		}
		if (value_num < value_before_num) {
			line += ` <i class="fa fa-arrow-down"></i>`;
		}
	}
	line += `</span>`;
	line += `<div class="tooltip-text">${tooltip_text}</div>`;
	line += `</div>`;
	return line;
}


function toggleCheckbox(name, clickedId) {
	const onCheckbox = document.getElementById(name + "_ON");
	const offCheckbox = document.getElementById(name + "_OFF");
	const inputField = document.getElementById("id_" + name);

	// Lógica para alternar los valores de los checkboxes
	if (clickedId === name + "_ON" && onCheckbox.checked) {
		offCheckbox.checked = false;
		inputField.value = "1";  // El valor será 1 cuando el primer checkbox está marcado
	} else if (clickedId === name + "_OFF" && offCheckbox.checked) {
		onCheckbox.checked = false;
		inputField.value = "2";  // El valor será 2 cuando el segundo checkbox está marcado
	}

	// Si ambos están desmarcados, el valor será 0
	if (!onCheckbox.checked && !offCheckbox.checked) {
		inputField.value = "0";
	}
}

