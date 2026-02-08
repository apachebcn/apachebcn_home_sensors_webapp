function getScale(objectId) {
    var value = null;
    if (!document.getElementById(objectId)) console.error("NOT " + objectId)
    if (document.getElementById(objectId).value !== null) {
        value = parseFloat(document.getElementById(objectId).value);
        if (value == 0) return null;
        return value;
    } else {
        console.error("objectID " + objectId + " NOT EXIST");
        return null;
    }
}

function getAxisType(configItemType, configItemFill) {
    var axisType = configItemType;
    if (axisType == 'line' && configItemFill) axisType = 'area';
    if (axisType == 'spline' && configItemFill) axisType = 'areaspline';
    return axisType;
}

function getLegendConfig() {
    if (!document.getElementById("id_legend_position")) return;
    if (!document.getElementById("id_legend_horizontal_align")) return;
    if (!document.getElementById("id_legend_vertical_align")) return;
    if (!document.getElementById("id_legend_enable")) return;
    return {
        layout: document.getElementById("id_legend_position").value, // 'horizontal' o 'vertical'
        align: document.getElementById("id_legend_horizontal_align").value, // 'left', 'center', 'right'
        verticalAlign: document.getElementById("id_legend_vertical_align").value, // 'top', 'middle', 'bottom'
        x: 0, // Ajusta según necesites
        y: 0, // Ajusta según necesites
        enabled: document.getElementById("id_legend_enable").checked // true o false
    };
}

function formatSerie(serie, objectId, isBoolean) {

    if (isBoolean) serie.yAxis = 0; else serie.yAxis = 1;

    if (!serie.hasOwnProperty('data')) {
        console.error(objectId + " has no data");
        return;
    }

    if (!Array.isArray(serie.data)) {
        console.error(objectId + " data is not array");
        return;
    }

    attr = "_visible";
    if (document.getElementById(objectId + attr) !== null) {
        serie.visible = document.getElementById(objectId + attr).checked;
    } else {
        console.error("objectID " + objectId + attr + " NOT EXIST");
        return serie;
    }

    attr = "_type";
    if (document.getElementById(objectId + attr) !== null && document.getElementById(objectId + "_fill") !== null) {
        serie.type = getAxisType(document.getElementById(objectId + attr).value, document.getElementById(objectId + "_fill").checked);
        console.log(objectId, serie.type);
        if (serie.type=="widebars") {
            // Aplicar configuración específica para widebars directamente a la serie
            serie.type = "column";
            serie.groupPadding = -0.1;
            serie.pointPadding = 0;
            serie.borderWidth = 0;
            serie.grouping = false;
        }
    } else {
        console.error("objectID " + objectId + "_type or _fill" + " NOT EXIST");
        return serie;
    }

    attr = "_opacity";
    if (document.getElementById(objectId + attr) !== null) {
        serie.fillOpacity = (document.getElementById(objectId + attr).value/100);
    } else {
        console.error("objectID " + objectId + attr + " NOT EXIST");
        return serie;
    }
 
    attr = "_color";
    if (document.getElementById(objectId + attr) !== null) {
        serie.color = document.getElementById(objectId + attr).value;
    } else {
        console.error("objectID " + objectId + attr + " NOT EXIST");
        return serie;
    }

    attr = "_points";
    if (document.getElementById(objectId + attr) !== null) {
        serie.marker = {enabled: document.getElementById(objectId + attr).checked};
    } else {
        console.error("objectID " + objectId + attr + " NOT EXIST");
        return serie;
    }

    if (isBoolean) {
        attr = "_value_on";
        if (document.getElementById(objectId + attr) !== null) {
            serie.data.forEach(point => {
                if (point[1] == "None" || point[1] == "NaN") {
                    point[1] = false;
                }
                else if (point[1] == 1) {
                    point[1]=(point[1]==1 ? parseFloat(document.getElementById(objectId + "_value_on").value) : 0);
                }
            });
        }
    } else {  // Convertir los valores "None" en false
        serie.data.forEach(point => {
            if (point[1] == "None" || point[1] == "NaN") {
                point[1] = false;
            }
        });
    }
}

// Función para vincular el evento input de los sliders con los outputs
function formatItemStyle(sliderId) {
    var slider = document.getElementById(sliderId);
    if (!slider) console.error("not " + sliderId)
    var output = document.getElementById('output-' + sliderId);
    if (!output) console.error("not output-" + sliderId)

    slider.addEventListener('input', function() {
        output.textContent = this.value + '%';
    });
}

// Función para formatear la fecha en el formato "%Y-%m-%dT%H:%M" manteniendo la zona horaria local
function formatDateForServer(dateString) {
    var date = new Date(dateString);
    var year = date.getFullYear();
    var month = ('0' + (date.getMonth() + 1)).slice(-2);
    var day = ('0' + date.getDate()).slice(-2);
    var hours = ('0' + date.getHours()).slice(-2);
    var minutes = ('0' + date.getMinutes()).slice(-2);
    var seconds = ('0' + date.getSeconds()).slice(-2);  // Añadir los segundos
    var milliseconds = ('00' + date.getMilliseconds()).slice(-3); // Obtener los milisegundos
    var formattedDate = `${year}-${month}-${day}T${hours}:${minutes}:${seconds}.${milliseconds}Z`;
    return formattedDate;
}

// Función para formatear la fecha y extraer la hora manteniendo la zona horaria local
function get_hour_from_dateString(dateString) {
    if (dateString instanceof Date) {
        dateString = dateString.toString();
    }
    if (typeof dateString !== 'string') {
        console.error("El valor proporcionado no es una cadena de texto");
        return null;
    }
    let time = dateString.match(/\d{2}:\d{2}:\d{2}/);
    return time ? time[0] : null;
}
