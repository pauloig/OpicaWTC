document.addEventListener('DOMContentLoaded', function () {
    const calendarContainer = document.getElementById('calendar');
    const calendarTitle = document.getElementById('calendar-title');

    const diasSemana = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    function generarEncabezadosDias() {
        const calendarDays = document.getElementById('calendar-days');
        calendarDays.innerHTML = '';  // Clear previous headers
        diasSemana.forEach(dia => {
            const diaDiv = document.createElement('div');
            diaDiv.className = 'day-header';
            diaDiv.innerText = dia;
            calendarDays.appendChild(diaDiv);
        });
    }

    function actualizarTituloCalendario(fecha) {
        const options = { month: 'long', year: 'numeric' };
        const titulo = fecha.toLocaleDateString('en-EN', options);
        calendarTitle.innerText = titulo.charAt(0).toUpperCase() + titulo.slice(1);
    }

    function parseCalendarList() {
        const calendarListElement = document.getElementById('calendar-list');
        const calendarList = JSON.parse(calendarListElement.value.replaceAll('(', '{').replaceAll(')', '}').replaceAll("'", '"').replaceAll(",]", "]"));
        return calendarList;
    }

    function applyColorToDayCell(diaDiv, hoursData) {
        const totalHours = hoursData.regular + hoursData.vacation + hoursData.sick + hoursData.holiday + hoursData.others;

       /* if (totalHours > 8) {
            console.error(`Total hours exceed 8 on day ${hoursData.day}.`);
            return;
        }
*/
        const regularPercent = (hoursData.regular / 8) * 100;
        const vacationPercent = (hoursData.vacation / 8) * 100;
        const sickPercent = (hoursData.sick / 8) * 100;
        const holidayPercent = (hoursData.holiday / 8) * 100;
        const othersPercent = (hoursData.others / 8) * 100;
        let divRegular = '';
        let divVacation = '';
        let divSick = '';
        let divHoliday = '';
        let divOthers = '';


        if (hoursData.regular > 0) {
            divRegular = `<div style="width: ${regularPercent}%; height: 100%; background-color: #4CAF50; color: white; display: flex; align-items: center; justify-content: start;">
                
            </div>`;
        }
        if (hoursData.vacation > 0) {
            divVacation = `<div style="width: ${vacationPercent}%; height: 100%; background-color: #2196F3; color: white; display: flex; align-items: center; justify-content: start;">
                
            </div>`;
        }
        if (hoursData.sick > 0) {
            divSick = ` <div style="width: ${sickPercent}%; height: 100%; background-color: #FFC107; color: black; display: flex; align-items: center; justify-content: start;">
                    
            </div>`;
        }
        if (hoursData.holiday > 0) {
            divHoliday = ` <div style="width: ${holidayPercent}%; height: 100%; background-color: #ff000c; color: black; display: flex; align-items: center; justify-content: start;">
                    
            </div>`;
        }
        if (hoursData.others > 0) {
            divOthers = ` <div style="width: ${othersPercent}%; height: 100%; background-color: #FF5722; color: white; display: flex; align-items: center; justify-content: start;">
                
            </div>`;
        }

        const periodID = document.getElementById('periodID').value;

        diaDiv.innerHTML = `
        <div style="display: flex; flex-direction: row; justify-content: center; width: 100%; height:100%">
            ${divRegular}   
            ${divVacation}   
            ${divSick}   
            ${divHoliday}   
            ${divOthers}                       
        </div>`;

        /*<div style="position:absolute; display: flex; flex-direction: column; justify-content: center; width: 20%;">
         ${hoursData.day}
         </div>  */


        const diaa = document.createElement('a');
        diaa.id = "dia_" + hoursData.day;
        diaa.setAttribute("hx-get", "/wtc/paidManuallyUpdate/" + periodID + "/" + hoursData.id);
        diaa.setAttribute("hx-target", "#dialog");
        diaa.style.position = "absolute";
        diaa.style.display = "flex";
        diaa.style.flexDirection = "column";
        diaa.style.justifyContent = "center";
        diaa.style.color = "black";
        /*diaa.style.height = "15%";
        diaa.style.width = "15%";*/
        diaa.innerHTML = hoursData.day;

        diaDiv.appendChild(diaa);


    }

    function fireHref(dia) {
        const ahref = document.getElementById("dia_" + dia);
        ahref.click();
    };

    function generarCalendario(fechaInicio, fechaFin) {
        calendarContainer.innerHTML = '';

        const fechaActual = new Date(fechaInicio.getFullYear(), fechaInicio.getMonth(), 1);
        const ultimoDiaDelMes = new Date(fechaInicio.getFullYear(), fechaInicio.getMonth() + 1, 0).getDate();
        const diasHabilitados = [];
        const fechaInicioRango = new Date(fechaInicio);
        const fechaFinRango = new Date(fechaFin);

        while (fechaInicioRango <= fechaFinRango) {
            diasHabilitados.push(fechaInicioRango.getDate());
            fechaInicioRango.setDate(fechaInicioRango.getDate() + 1);
        }

        const primerDiaDelMes = new Date(fechaInicio.getFullYear(), fechaInicio.getMonth(), 1).getDay();

        for (let i = 0; i < primerDiaDelMes; i++) {
            const emptyDiv = document.createElement('div');
            emptyDiv.className = 'calendar-cell empty';
            calendarContainer.appendChild(emptyDiv);
        }

        const calendarList = parseCalendarList();

        const periodID = document.getElementById('periodID').value;

        for (let dia = 1; dia <= ultimoDiaDelMes; dia++) {
            const diaDiv = document.createElement('div');
            diaDiv.className = 'calendar-cell';
            diaDiv.addEventListener('click', function () {
                fireHref(dia);
            });



            if (diasHabilitados.includes(dia)) {
                diaDiv.classList.add('enabled');

                const diaa = document.createElement('a');
                diaa.id = "dia_" + dia;
                diaa.setAttribute("hx-get", "/wtc/paidManually/" + periodID + "/" + dia);
                diaa.setAttribute("hx-target", "#dialog");
                diaa.innerHTML = dia;

                diaDiv.appendChild(diaa);

                const dayData = calendarList.find(item => item.day === dia);
                if (dayData) {
                    applyColorToDayCell(diaDiv, dayData);
                }

            } else {

                diaDiv.classList.add('disabled');
                diaDiv.innerText = dia;

            }



            calendarContainer.appendChild(diaDiv);

        }

        actualizarTituloCalendario(fechaInicio);
    }


    generarEncabezadosDias();

    const iDate = document.getElementById('iDate');
    const finalDate = document.getElementById('fDate');


    const fechaInicio = new Date(iDate.value);
    const fechaFin = new Date(finalDate.value);


    generarCalendario(fechaInicio, fechaFin);
});
