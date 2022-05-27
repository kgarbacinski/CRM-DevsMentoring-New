
const noteUrl = '/api/get-note/?id='
let meetingDates = function (startDate, endDate){
    return `/api/meetings-range/?start_date=${startDate}&end_date=${endDate}`
}

document.addEventListener('DOMContentLoaded', function () {
    displayAllMeetings()
}, false);


function showNoteText(id_obj, element) {
    getJson(noteUrl + id_obj)
        .then(data => {
            console.log(data);
            if (data.length > 0) {
                element.innerHTML =  data[0].text
            }
        })
}

function displayAllMeetings() {
    if (sessionStorage.getItem('isMentor') === 'true') {
        let futureDates = getFutureDates(7);
        let querySelector = document.querySelector('.mentor-page .mentor-page-block');
        getMeetings(futureDates, true, querySelector);
    } else {
        let futureDates = getFutureDates(7);
        let pastDates = getBackDates(30);
        let querySelector = document.querySelector('.student-page .incoming-meetings .student-page-block');
        getMeetings(futureDates, false, querySelector);
        querySelector = document.querySelector('.student-page .last-meetings .student-page-block');
        getMeetings(pastDates, false, querySelector, false);
    }
}

function getMeetings(dates, isMentor, querySelector, showCalendarButton = true) {
    let startDate = dates.start_date;
    let endDate = dates.end_date;
    getJson(meetingDates(startDate, endDate))
        .then(data => {
            data.forEach(meeting => {
                let div = createElement('div', querySelector, {className: 'meet-box'}),
                    p = createElement('p', div, {className: 'meet-details'}),
                    span = createElement('span', p, {className: 'date'});
                createElement('i', span, {className: 'bi bi-calendar-check',});
                span.append(meeting.date.split("-").reverse().join("."));
                let span2 = createElement('span', p, {className: 'hour', textContent: meeting.hour})
                createElement('i', span2, {className: 'bi bi-clock'})

                let p2 = createElement('p', div);
                createElement('i', p2, {className: 'bi bi-person-square'})
                createElement('span', p2, {
                    className: 'student-name',
                    textContent: isMentor ? meeting.student_name : meeting.mentor_name
                })
                if (!showCalendarButton) showNoteText(meeting.id, p2)
            })
            if (showCalendarButton) {
                let calendarButton = createElement('div', querySelector, {className: 'control-btn'})
                createElement('a', calendarButton, {
                    className: 'button', href: "/calendar/",
                    textContent: 'show calendar'
                })
            }
        }).catch((error => {console.log(error)}))
}