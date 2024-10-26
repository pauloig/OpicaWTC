window.onload = function () {
  startTime();


}

function startTime() {
  const today = new Date();
  let h = today.getHours();
  let m = today.getMinutes();
  let s = today.getSeconds();
  m = checkTime(m);
  s = checkTime(s);

  dayString = new Date(today.toJSON().slice(0, 10)).toLocaleString('en-us', { weekday: 'long' });
  monthString = new Date(today.toJSON().slice(0, 10)).toLocaleString('en-us', { month: 'long' });
  dayNumber = new Date(today.toJSON().slice(0, 10)).toLocaleString('en-us', { day: 'numeric' });

  document.getElementById('date').innerHTML = dayString + ", " + monthString + " " + dayNumber;
  document.getElementById('hour').innerHTML = h + ":" + m + ":" + s;

  setTimeout(startTime, 1000);
}

function checkTime(i) {
  if (i < 10) { i = "0" + i };  // add zero in front of numbers < 10
  return i;
}


function enterDigit(digit) {
  event.preventDefault();
  const pinBox = document.getElementById('pinBox');
  if (pinBox.value.length < 3) {
    pinBox.value += digit;
  }
  toggleSearchButton();
}

function clearDigit() {
  event.preventDefault();
  const pinBox = document.getElementById('pinBox');
  pinBox.value = pinBox.value.slice(0, -1);
  toggleSearchButton();
}

function clearAll() {
  event.preventDefault();
  const pinBox = document.getElementById('pinBox');
  pinBox.value = "";
  toggleSearchButton();
}

function toggleSearchButton() {
  event.preventDefault();
  const pinBox = document.getElementById('pinBox');
  const searchButton = document.getElementById('searchButton');

  if (pinBox.value.length === 3) {
    searchButton.disabled = false;
  } else {
    searchButton.disabled = true;
  }
}

function login() {
  event.preventDefault();
  const pinBox = document.getElementById('pinBox').value;
  document.getElementById("idNumber").value = pinBox;
  document.getElementById("login").submit();
  //alert("Logging in with PIN: " + pinBox);
  // Redirect to another page or handle login logic here
}


// PBTH FUNCTIONS

function clockIn() {
  event.preventDefault();

  const employeeID = document.getElementById('employeeID').value;

  const clockInTime = document.getElementById('clockInTime');
  clockInTime.textContent = getCurrentTime();



  window.location.href = "/wtc/pbth_setTime/0/" + employeeID + "/1/"
}

function clockOut() {
  event.preventDefault();
  const clockOutTime = document.getElementById('clockOutTime');
  clockOutTime.textContent = getCurrentTime();



  const employeeID = document.getElementById('employeeID').value;
  const wtcID = document.getElementById('wtcID').value;
  window.location.href = "/wtc/pbth_setTime/" + wtcID + "/" + employeeID + "/2/"
}

function breakOut() {
  event.preventDefault();
  const breakOutTime = document.getElementById('breakOutTime');
  breakOutTime.textContent = getCurrentTime();

  const employeeID = document.getElementById('employeeID').value;
  const wtcID = document.getElementById('wtcID').value;
  window.location.href = "/wtc/pbth_setTime/" + wtcID + "/" + employeeID + "/3/"
}

function breakIn() {
  event.preventDefault();
  const breakInTime = document.getElementById('breakInTime');
  breakInTime.textContent = getCurrentTime();

  const employeeID = document.getElementById('employeeID').value;
  const wtcID = document.getElementById('wtcID').value;
  window.location.href = "/wtc/pbth_setTime/" + wtcID + "/" + employeeID + "/4/"
}

function lunchOut() {
  event.preventDefault();
  const lunchOutTime = document.getElementById('lunchOutTime');
  lunchOutTime.textContent = getCurrentTime();

  const employeeID = document.getElementById('employeeID').value;
  const wtcID = document.getElementById('wtcID').value;
  window.location.href = "/wtc/pbth_setTime/" + wtcID + "/" + employeeID + "/5/"
}

function lunchIn() {
  event.preventDefault();
  const lunchInTime = document.getElementById('lunchInTime');
  lunchInTime.textContent = getCurrentTime();

  const employeeID = document.getElementById('employeeID').value;
  const wtcID = document.getElementById('wtcID').value;
  window.location.href = "/wtc/pbth_setTime/" + wtcID + "/" + employeeID + "/6/"
}

function getCurrentTime() {
  event.preventDefault();
  const now = new Date();
  return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function toggleGroup(groupId) {

  event.preventDefault();
  const group = document.getElementById(groupId);
  if (group.classList.contains('hidden')) {
    group.classList.remove('hidden');
  } else {
    group.classList.add('hidden');
  }
}
