const today = new Date().toISOString().split('T')[0];
const pickedAppointmentDate = document.getElementById('appointment_date');
const getAppointmentButton = document.getElementById('get_appointment');
const businessId = document.getElementById("business_id").value;
const appoinmentForm = document.getElementById('appointment_form');
pickedAppointmentDate.setAttribute("min", today);
pickedAppointmentDate.value = today;

const appointmentFormData = (data) => {
    let output = ""
    data.forEach(ele => {
        output += `<input type="radio" class="btn-check" name="appointment_time" id="${ele}" autocomplete="off" value="${ele}"><label class="btn" for="${ele}">${convertTo12HourFormat(ele)}</label>`;
        console.log(ele);
    });
    output += `<button type="submit" class="btn btn-outline-primary d-block mx-auto mt-3" name="appointment_confirm" value="True">Confirm</button>`;
    appoinmentForm.innerHTML = output;
};

getAppointmentButton.addEventListener("click", () => {
    if (pickedAppointmentDate.value) {
        fetch(`/salon/business/appointment/check/${businessId}/${pickedAppointmentDate.value}`).
        then(res => res.json()).
        then(res => {
            getAppointmentButton.disabled = true;
            pickedAppointmentDate.disabled = true;
            document.getElementById('appointment_date_confirmation').value = pickedAppointmentDate.value;
            appointmentFormData(res.data);
        })
    }
});

function convertTo12HourFormat(timeString) {
    let timeParts = timeString.split(":");
    let hours = parseInt(timeParts[0], 10);
    let minutes = parseInt(timeParts[1], 10);
    let period = hours >= 12 ? 'PM' : 'AM';
    
    hours = hours % 12;
    hours = hours ? hours : 12;
    minutes = minutes < 10 ? '0' + minutes : minutes;
    let formattedTime = hours + ':' + minutes + ' ' + period;
    
    return formattedTime;
}
