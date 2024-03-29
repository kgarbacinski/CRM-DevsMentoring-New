let today = new Date(),
    currentMonth = today.getMonth(),
    currentYear = today.getFullYear();

const footerYear = document.querySelector('.year');
const myFileBtn = document.getElementById('myFile');
const fileChosen = document.getElementById('file-chosen');
const changeAvBtn = document.getElementById('change-avatar')
const avatar = document.getElementById('avatar')

const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
];
document.addEventListener('DOMContentLoaded', function () {
    showYear()
}, false);

changeAvBtn.addEventListener('click', (event) => {
    event.preventDefault();
    changeAvatar();
})

myFileBtn.addEventListener('change', function () {
    fileChosen.textContent = this.files[0].name;
})

function daysInMonth(iMonth, iYear) {
    return 32 - new Date(iYear, iMonth, 32).getDate();
}

async function getJson(url) {
    const response = await fetch(getBaseUrl(url));
    return (await response).json()
}

function getFutureDates(days) {
    let start = `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()} ${today.getHours()}:${today.getMinutes()}`;
    let end = addDays(today, days);
    let end_date = `${end.getFullYear()}-${end.getMonth() + 1}-${end.getDate()} ${end.getHours()}:${end.getMinutes()}`;
    return {start_date: start, end_date: end_date}
}

function getBackDates(days) {
    let start = subDays(today, days)
    let start_date = `${start.getFullYear()}-${start.getMonth() + 1}-${start.getDate()} ${start.getHours()}:${start.getMinutes()}`
    let end_date = `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()} ${today.getHours()}:${today.getMinutes()}`
    return {start_date: start_date, end_date: end_date}
}

function addDays(date, days) {
    let result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}

function subDays(date, days) {
    let result = new Date(date);
    result.setDate(result.getDate() - days);
    return result;
}

function getBaseUrl(path) {
    let protocol = window.location.protocol;
    let host = window.location.host;
    return `${protocol}//${host ? host : ""}${path}`
}

function createElement(element, elem, args) {
    let d = document.createElement(element);
    if (args) for (const [k, v] of Object.entries(args)) d[k] = v;
    elem.appendChild(d);
    return d;
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function showYear() {
    const data = new Date();
    footerYear.textContent = data.getFullYear().toString();
}



function changeAvatar() {
    let input = document.querySelector('input[type="file"]');
    let userId = sessionStorage.getItem('mentorId');
    let data = new FormData();
    data.append('id', userId);
    data.append('user_image', input.files[0]);
    let url = getBaseUrl('/api/change-avatar/' + userId + '/');
    let userImage = document.getElementById('user-avatar');

    setAvatar(url, data)
        .then(data =>{
            userImage.src = data.user_image;
        })
}

async function setAvatar(url = '', data = {}) {
    const response = await fetch(url, {
        method: "PATCH",
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: data,
    });
    return response.json()
}

function setOptionsToNull() {
    Array.from(arguments).forEach(argument => {
        for (let option = argument.options.length - 1; option >= 0; option--) {
            argument.options[option] = null;
        }
    })
}

function removeAttribute(elem, attr) {
    Array.from(elem.options).forEach(option => {
        option.removeAttribute(attr)
    })
}

function setOptionToSelected(elem, attr) {
    Array.from(elem.options).forEach(option => {
        if (option.value === attr) {
            option.setAttribute('selected', 'selected')
        }
    })
}

function setAttributes(elem, attrs) {
    for (let key in attrs) {
        elem.setAttribute(key, attrs[key]);
    }
}

function cleanSendData(value = null) {
    if (!value) {
        for (let element in sendData) {
            sendData[element] = ''
        }
        return
    }
    sendData[value] = '';
}

function getApiUrl() {
    let url = '?'
    for (let sendDataKey in sendData) {
        if (sendData[sendDataKey]) {
            url += `${sendDataKey}=${sendData[sendDataKey]}&`
        }
    }
    return url
}

