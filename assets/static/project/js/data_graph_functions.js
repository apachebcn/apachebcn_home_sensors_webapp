
function getLegendConfig() {

    return {
        layout: "horizontal", // 'horizontal' o 'vertical'
        align: "right", // 'left', 'center', 'right'
        verticalAlign: "top", // 'top', 'middle', 'bottom'
        x: 0, // Ajusta según necesites
        y: 0, // Ajusta según necesites
        enabled: true // true o false
    };
}

function formatSerie(serie, objectId) {

    serie.yAxis = 1;

    if (!serie.hasOwnProperty('data')) {
        console.error(objectId + " has no data");
        return;
    }

    if (!Array.isArray(serie.data)) {
        console.error(objectId + " data is not array");
        return;
    }

    serie.visible = true;
    serie.type = "line";
    serie.opacity = 1;
    serie.color = null;
    serie.points = false;

    // Convertir los valores "None" en false
    serie.data.forEach(point => {
        if (point[1] == "None" || point[1] == "NaN") {
            point[1] = false;
        }
    });
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
