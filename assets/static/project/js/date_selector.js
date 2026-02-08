document.addEventListener('DOMContentLoaded', function() {
    // Obtener referencias a los elementos HTML
    const startInput = document.getElementById('start_local_date_str');
    const endInput = document.getElementById('end_local_date_str');
    const dailyButton = document.getElementById('daily');
    const weeklyButton = document.getElementById('weekly');
    const monthlyButton = document.getElementById('monthly');
    const halfmonthlyButton = document.getElementById("halfmonthly")
    const yearlyButton = document.getElementById('yearly');

    // Función para formatear una fecha en formato YYYY-MM-DDTHH:MM
    function formatDateTime(date) {
        const year = date.getFullYear();
        const month = ('0' + (date.getMonth() + 1)).slice(-2);
        const day = ('0' + date.getDate()).slice(-2);
        const hours = ('0' + date.getHours()).slice(-2);
        const minutes = ('0' + date.getMinutes()).slice(-2);
        return `${year}-${month}-${day}T${hours}:${minutes}`;
    }

    // Función para establecer las fechas según el tipo de intervalo seleccionado
    function setDates(interval) {
        const today = new Date(); // Obtener la fecha actual

        // Establecer la fecha de fin como hoy a las 23:59:59
        const endOfDay = new Date(today);
        endOfDay.setHours(23, 59, 59, 999); // Establecer la hora final del día
        switch (interval) {
            case 'daily':
                // Para el intervalo diario, establecer inicio a las 00:00 y fin a las 23:59
                const startOfDay = new Date(today);
                startOfDay.setHours(0, 0, 0, 0); // Establecer la hora inicial del día
                startInput.value = formatDateTime(startOfDay);
                endInput.value = formatDateTime(endOfDay);
                break;
            case 'weekly':
                // Calcular la fecha de inicio de la semana (lunes)
                const startOfWeek = getStartOfWeek(today);
                startInput.value = formatDateTime(startOfWeek);
                const endOfWeek = getEndOfWeek(today);
                endInput.value = formatDateTime(endOfWeek);
                break;

            case 'halfmonthly':
                // Calcular el inicio del mes actual
                const startOfHalfMonth = getStartOfHalfMonth(today);
                startInput.value = formatDateTime(startOfHalfMonth);
                const endOfHalfMonth = getEndOfHalfMonth(today);
                endInput.value = formatDateTime(endOfHalfMonth);
                break;


                case 'monthly':
                // Calcular el inicio del mes actual
                const startOfMonth = getStartOfMonth(today);
                startInput.value = formatDateTime(startOfMonth);
                const endOfMonth = getEndOfMonth(today);
                endInput.value = formatDateTime(endOfMonth);
                break;
            case 'yearly':
                // Calcular el inicio del año actual
                const startOfYear = getStartOfYear(today);
                startInput.value = formatDateTime(startOfYear);
                const endOfYear = getEndOfYear(today);
                endInput.value = formatDateTime(endOfYear);
                console.log(endInput.value);
                break;
            default:
                break;
        }
    }

    // Función para obtener el inicio de la semana (lunes)
    function getStartOfWeek(date) {
        const startOfWeek = new Date(date);
        const dayOfWeek = startOfWeek.getDay();
        const diff = startOfWeek.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1);
        startOfWeek.setDate(diff);
        startOfWeek.setHours(0, 0, 0, 0); // Establecer la hora inicial del día
        return startOfWeek;
    }

    // Función para obtener el final de la semana (domingo)
    function getEndOfWeek(date) {
        const endOfWeek = new Date(date);
        const dayOfWeek = endOfWeek.getDay();
        const diff = endOfWeek.getDate() - dayOfWeek + (dayOfWeek === 0 ? 0 : 7);
        endOfWeek.setDate(diff);
        endOfWeek.setHours(23, 59, 59, 999); // Último milisegundo del día
        return endOfWeek;
    }

    // Función para obtener el inicio del mes
    function getStartOfMonth(date) {
        const startOfMonth = new Date(date);
        startOfMonth.setDate(1);
        startOfMonth.setHours(0, 0, 0, 0); // Establecer la hora inicial del día
        return startOfMonth;
    }

    // Función para obtener el final del mes
    function getEndOfMonth(date) {
        const endOfMonth = new Date(date);
        endOfMonth.setMonth(endOfMonth.getMonth() + 1, 0); // Día 0 del siguiente mes = último día del mes actual
        endOfMonth.setHours(23, 59, 59, 999); // Último milisegundo del día
        return endOfMonth;
    }

    // Función para obtener el inicio del semestre (primer o segundo semestre del año)
    function getStartOfHalfMonth(date) {
        const startOfHalfMonth = new Date(date);
        const month = startOfHalfMonth.getMonth(); // Obtiene el mes actual (0-11)

        // Si el mes es enero a junio (0-5), devuelve el 1 de enero (inicio del primer semestre)
        if (month < 6) {
            startOfHalfMonth.setMonth(0);  // Establece el mes a enero
            startOfHalfMonth.setDate(1);   // Establece el día a 1
        } else {
            startOfHalfMonth.setMonth(6);  // Establece el mes a julio
            startOfHalfMonth.setDate(1);   // Establece el día a 1
        }

        startOfHalfMonth.setHours(0, 0, 0, 0); // Establece la hora inicial del día
        return startOfHalfMonth;
    }

    // Función para obtener el final del semestre (primer o segundo semestre del año)
    function getEndOfHalfMonth(date) {
        const endOfHalfMonth = new Date(date);
        const month = endOfHalfMonth.getMonth(); // mes actual (0-11)

        if (month < 6) {
            // Primer semestre: último día de junio
            endOfHalfMonth.setMonth(5);  // junio (mes 5)
            endOfHalfMonth.setDate(30);  // último día de junio
        } else {
            // Segundo semestre: último día de diciembre
            endOfHalfMonth.setMonth(11); // diciembre (mes 11)
            endOfHalfMonth.setDate(31);  // último día de diciembre
        }

        endOfHalfMonth.setHours(23, 59, 59, 999); // último milisegundo del día
        return endOfHalfMonth;
    }

    // Función para obtener el inicio del año
    function getStartOfYear(date) {
        const startOfYear = new Date(date);
        startOfYear.setMonth(0); // Enero es el mes 0
        startOfYear.setDate(1);
        startOfYear.setHours(0, 0, 0, 0); // Establecer la hora inicial del día
        return startOfYear;
    }

    // Función para obtener el final del año
    function getEndOfYear(date) {
        const endOfYear = new Date(date);
        endOfYear.setMonth(11); // Diciembre es el mes 11
        endOfYear.setDate(31);
        endOfYear.setHours(23, 59, 59, 999); // Último milisegundo del día
        return endOfYear;
    }

    // Función para ajustar la fecha de inicio y fin al restar o sumar días
    function adjustDates(adjustment) {
        let startDate = new Date(startInput.value);
        let endDate = new Date(endInput.value);

        if (isNaN(startDate.getTime()) || isNaN(endDate.getTime())) {
            console.warn('Invalid date format');
            return;
        }

        // Ajustar las fechas
        startDate.setDate(startDate.getDate() + adjustment);
        endDate.setDate(endDate.getDate() + adjustment);

        // Establecer los valores de las fechas en los inputs
        startInput.value = formatDateTime(startDate);
        endInput.value = formatDateTime(endDate);
    }

    // Función para ajustar las fechas mensuales
    function adjustMonthlyDates(adjustment) {
        let startDate = new Date(startInput.value);
        let endDate = new Date(endInput.value);

        if (isNaN(startDate.getTime()) || isNaN(endDate.getTime())) {
            console.warn('Invalid date format');
            return;
        }

        // Ajustar los meses
        startDate.setMonth(startDate.getMonth() + adjustment);
        endDate.setMonth(endDate.getMonth() + adjustment);

        // Establecer los valores de las fechas en los inputs
        startInput.value = formatDateTime(startDate);
        endInput.value = formatDateTime(endDate);
    }

    // Función para ajustar las fechas anuales
    function adjustYearlyDates(adjustment) {
        let startDate = new Date(startInput.value);
        let endDate = new Date(endInput.value);

        if (isNaN(startDate.getTime()) || isNaN(endDate.getTime())) {
            console.warn('Invalid date format');
            return;
        }

        // Ajustar los años
        startDate.setFullYear(startDate.getFullYear() + adjustment);
        endDate.setFullYear(endDate.getFullYear() + adjustment);

        // Establecer los valores de las fechas en los inputs
        startInput.value = formatDateTime(startDate);
        endInput.value = formatDateTime(endDate);
    }


    function form_submit() {
        var form = document.getElementById('form_data_graph');
        if (form) {
            form.submit();
        }
    }

    // Botón ajustar a hoy
    dailyButton.addEventListener('click', function() {
        setDates('daily');
        form_submit();
    });

    // Botón ajustar a esta semana
    weeklyButton.addEventListener('click', function() {
        setDates('weekly');
        form_submit();
    });

    // Botón ajustar a este mes
    monthlyButton.addEventListener('click', function() {
        setDates('monthly');
        form_submit();
    });

    // Botón ajustar a este semestre
    halfmonthlyButton.addEventListener('click', function() {
        setDates('halfmonthly');
        form_submit();
    });

    // Botón ajustar a este año
    yearlyButton.addEventListener('click', function() {
        setDates('yearly');
        form_submit();
    });

    // Ajusatar a 1 días menos
    document.getElementById('daily-minus').addEventListener('click', function() {
        adjustDates(-1);
        form_submit();
    });

    // Ajusatar a 1 días más
    document.getElementById('daily-plus').addEventListener('click', function() {
        adjustDates(1);
        form_submit();
    });

    // Ajusatar a 1 semana menos
    document.getElementById('weekly-minus').addEventListener('click', function() {
        adjustDates(-7);
        form_submit();
    });

    // Ajusatar a 1 semana más
    document.getElementById('weekly-plus').addEventListener('click', function() {
        adjustDates(7);
        form_submit();
    });

    // Ajusatar a 1 mes menos
    document.getElementById('monthly-minus').addEventListener('click', function() {
        adjustMonthlyDates(-1);
        form_submit();
    });

    // Ajusatar a 1 mes más
    document.getElementById('monthly-plus').addEventListener('click', function() {
        adjustMonthlyDates(1);
        form_submit();
    });


    // Ajusatar a 1 mes menos
    document.getElementById('halfmonthly-minus').addEventListener('click', function() {
        adjustMonthlyDates(-6);
        form_submit();
    });

    // Ajusatar a 1 mes más
    document.getElementById('halfmonthly-plus').addEventListener('click', function() {
        adjustMonthlyDates(6);
        form_submit();
    });

    // Ajusatar a 1 año menos
    document.getElementById('yearly-minus').addEventListener('click', function() {
        adjustYearlyDates(-1);
        form_submit();
    });

    // Ajusatar a 1 año más
    document.getElementById('yearly-plus').addEventListener('click', function() {
        adjustYearlyDates(1);
        form_submit();
    });



});
