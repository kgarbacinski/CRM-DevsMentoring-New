class Selectors {
    static themeName = document.querySelectorAll('a.theme-name.available');
    static themeDetails = document.querySelector('.themes-details');
    static backBtn = document.querySelector('.back-btn');
    static fileDetails = Selectors.themeDetails.children;
    static tittle = Selectors.fileDetails.namedItem('tittle');
    static description = Selectors.fileDetails.namedItem('description');
    static filesContainer = Selectors.fileDetails.namedItem('container');
    static filesList = Selectors.filesContainer.children.namedItem('filesListContainer').children.namedItem('filesList');
    static AccessUsersListForOneSubTopic = document.getElementsByClassName("shared-for-student-list")[0].children.namedItem("shared_for_one");
    static NotAccessUsersListForOneSubTopic = document.getElementsByClassName("sharing-student-list")[0].children.namedItem("share_for_one");
    static ThemeNameForOne = document.getElementsByClassName("theme-name").namedItem('tittle_modal_for_one');
    static ThemeNameForSubject = document.getElementsByClassName("category-name").namedItem("tittle_modal_for_subject");
    static AccessUsersListForSubject = document.getElementsByClassName("shared-for-student-list")[1].children.namedItem("shared_for_all");
    static NotAccessUsersListForSubject = document.getElementsByClassName("sharing-student-list")[1].children.namedItem("share_for_all");
    static curr_topic = "";
    static curr_subject = "";
    static searchShared = document.querySelector('.search-shared-for');
    static csrftoken = getCookie('csrftoken');
    static searchSharing = document.querySelector('.search-sharing');
    static liSharing = document.querySelectorAll('.sharing-student-name');
    static liShared = document.querySelectorAll('.shared-for-student-name');
}


// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
let user_id = '';
let user_first_name = '';
let user_last_name = '';
let access = '';

const toggleDetails = () => {
    // Selectors.themeDetails.style.visibility = 'visible';
    if (Selectors.themeDetails.style.display === "none") {
        Selectors.themeDetails.style.display = "block";
    } else {
        Selectors.themeDetails.style.display = "none";
    }
}

const showDetails = () => {
    // if (Selectors.themeDetails.style.display == "none") {
    Selectors.themeDetails.style.display = "block"
    // }
}

const closeDetails = () => {
    // if (Selectors.themeDetails.style.display == "block") {
    Selectors.themeDetails.style.display = "none"
    // }
}

//TODO sprawdzić czy
Selectors.themeName.forEach(name => name.addEventListener('click', () => {
    getFiles(name.id)
        .then(showDetails)
}))
Selectors.backBtn.addEventListener('click', closeDetails)

// js for search engines in modals:

// 1- shared for:


// const searchEngine = (e) => {
//     const text = e.target.value.toLowerCase();
//     console.log(e)
//     Selectors.liShared.forEach(el => {
//
//         if (el.textContent.toLowerCase().indexOf(text) !== -1) {
//             el.style.display = 'block'
//         } else {
//             el.style.display = 'none'
//         }
//     })
// }

// Selectors.searchShared.addEventListener('keyup', searchEngine)


Selectors.searchShared.addEventListener('keyup', (e) => {
    const text = e.target.value.toLowerCase();
    searchEngine(Selectors.liShared, text)
});

// 2- sharing:

function searchEngine(selector, text) {
    // const text = aa.target.value.toLowerCase();
    selector.forEach(el => {
        if (el.textContent.toLowerCase().indexOf(text) !== -1) {
            el.style.display = 'block'
        } else {
            el.style.display = 'none'
        }

    })
}

//
// const searchEngine2 = (e) => {
//     const text = e.target.value.toLowerCase();
//     Selectors.liSharing.forEach(el => {
//
//         if (el.textContent.toLowerCase().indexOf(text) !== -1) {
//             el.style.display = 'block'
//         } else {
//             el.style.display = 'none'
//         }
//     })
// }
// Selectors.searchSharing.addEventListener('keyup', searchEngine2)

Selectors.searchSharing.addEventListener('keyup,', (e) => {
    const text = e.target.value.toLowerCase();
    searchEngine(Selectors.liSharing, text)
})


// TODO api address to check
async function getFiles(topic_id) {
    let url = (getBaseUrl('/files/api/files/') + topic_id)
    let response = await fetch(url);
    if (response.ok) {
        let files = await response.json();
        Selectors.filesList.innerHTML = '';
        // Selectors.themeDetails.style.visibility = 'visible';
        Selectors.tittle.innerHTML = files[0].subtopic_name;
        Selectors.description.innerHTML = files[0].subtopic_description;
        // toggleDetails();
        files.forEach(obj => {
            let a = document.createElement('a');
            a.href = obj.file
            a.innerHTML = `<i class="bi bi-file-earmark-arrow-down"></i><span class="file-name">${obj.name} - ${obj.type} </span>`
            Selectors.filesList.appendChild(a)
        });
    }
}


function CreateHtmlForUserTable(access, type) {
    let li = document.createElement('li');
    let p = document.createElement('p');
    let button = document.createElement("button");
    let i = document.createElement('i')
    p.className = 'student-name'
    button.className = "student-delete"
    p.innerHTML = user_first_name + " " + user_last_name

    switch (access) {
        case true:
            i.className = "bi bi-dash-lg"
            if (type === "topic") {
                button.addEventListener("click", deleteUserToOneSubTopic.bind(null, user_id, Selectors.curr_topic));
            } else if (type === 'subject') {
                button.addEventListener("click", deleteUserToSubject.bind(null, user_id, Selectors.curr_subject));
            }
            break

        case false:
            i.className = "bi bi-plus-lg"
            if (type === "topic") {
                button.addEventListener("click", addUserToOneSubTopic.bind(null, user_id, Selectors.curr_topic));
            } else if (type === 'subject') {
                button.addEventListener("click", addUserToSubject.bind(null, user_id, Selectors.curr_subject));
            }
            break;
    }

    button.appendChild(i)
    p.appendChild(button)
    li.appendChild(p)
    return li

}

function getAllUsersForOneTopic(topic_id) {
    getJson('/files/api/access/files/' + topic_id)
        .then(users => {
            Selectors.curr_topic = topic_id;
            Selectors.AccessUsersListForOneSubTopic.innerHTML = '';
            Selectors.NotAccessUsersListForOneSubTopic.innerHTML = '';
            Selectors.ThemeNameForOne.innerHTML = users[0].subtopic_name;
            let access = '';
            users.forEach(obj => {
                Object.entries(obj).forEach(([key, value]) => {
                    user_id = obj.id
                    user_first_name = obj.first_name
                    user_last_name = obj.last_name
                    access = obj.access
                });
                if (access) {
                    let li = CreateHtmlForUserTable(true, 'topic')
                    Selectors.AccessUsersListForOneSubTopic.appendChild(li)

                } else {

                    let li = CreateHtmlForUserTable(false, 'topic')
                    Selectors.NotAccessUsersListForOneSubTopic.appendChild(li)

                }
            });
        })
}

async function addUserToOneSubTopic(user_id, topic_id) {
    let url = (window.location.origin + '/files/api/access/files/' + topic_id + "/")
    const config = {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': Selectors.csrftoken

        },
        body: JSON.stringify(user_id),
    }
    const response = await fetch(url, config)
    if (response.ok) {
        await getAllUsersForOneTopic(topic_id)

    }
}

async function deleteUserToOneSubTopic(user_id, topic_id) {
    let url = (window.location.origin + '/files/api/access/files/' + topic_id + "/")
    const config = {
        method: 'DELETE',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': Selectors.csrftoken

        },
        body: JSON.stringify(user_id),
    }
    const response = await fetch(url, config)
    if (response.ok) {
        await getAllUsersForOneTopic(topic_id)
    }
}


async function getUsersSubject(subject_id) {
    let url = (window.location.origin + 'files/api/access/subject/' + subject_id)
    Selectors.curr_subject = subject_id
    let response = await fetch(url);
    if (response.ok) {
        let users = await response.json();
        Selectors.AccessUsersListForSubject.innerHTML = ''
        Selectors.NotAccessUsersListForSubject.innerHTML = ''
        Selectors.ThemeNameForSubject.innerHTML = users[0].subject_name
        users.forEach(obj => {
            Object.entries(obj).forEach(([key, value]) => {
                user_id = obj.id
                user_first_name = obj.first_name
                user_last_name = obj.last_name
                access = obj.access
            });
            if (access) {
                let li = CreateHtmlForUserTable(true, 'subject')
                Selectors.AccessUsersListForSubject.appendChild(li)
            } else {
                let li = CreateHtmlForUserTable(false, 'subject')
                Selectors.NotAccessUsersListForSubject.appendChild(li)
            }
        });
    }


}


async function addUserToSubject(user_id, subject_id) {
    let url = (window.location.origin + '/files/api/access/subject/' + subject_id + "/")
    const config = {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': Selectors.csrftoken

        },
        body: JSON.stringify(user_id),
    }
    const response = await fetch(url, config)
    if (response.ok) {
        await getUsersSubject(subject_id)

    }
}


async function deleteUserToSubject(user_id, subject_id) {
    let url = (window.location.origin + '/files/api/access/subject/' + subject_id + "/")
    const config = {
        method: 'DELETE',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': Selectors.csrftoken

        },
        body: JSON.stringify(user_id),
    }
    const response = await fetch(url, config)
    if (response.ok) {
        await getUsersSubject(subject_id)
    }
}

async function getSharedUsersSearchBoxSubtopic() {
    let text = document.getElementById('search-shared-for-topic')
    if (text) {
        let url = (window.location.origin + '/files/api/access/searchbox/topic/' + Selectors.curr_topic + "/" + "?text=" + text + "&access=1"
        )
        let response = await fetch(url);
        if (response.ok) {
            let users = await response.json();
            Selectors.AccessUsersListForOneSubTopic.innerHTML = ''
            users.forEach(obj => {
                Object.entries(obj).forEach(([key, value]) => {
                    user_id = obj.id
                    user_first_name = obj.first_name
                    user_last_name = obj.last_name
                });
                let li = CreateHtmlForUserTable(true, 'topic')
                Selectors.AccessUsersListForOneSubTopic.appendChild(li)
            })
        }

    } else {
        await getAllUsersForOneTopic(Selectors.curr_topic)
    }
}


async function GetNotSharedUsersSearchBoxSubtopic() {
    let text = document.getElementById('search-sharing-topic')
    if (text) {
        let url = (window.location.origin + '/files/api/access/searchbox/topic/' + Selectors.curr_topic + "/" + "?text=" + text + "&access=0"
        )
        let response = await fetch(url);
        if (response.ok) {
            let users = await response.json();
            Selectors.NotAccessUsersListForOneSubTopic.innerHTML = ''
            users.forEach(obj => {
                Object.entries(obj).forEach(([key, value]) => {
                    user_id = obj.id
                    user_first_name = obj.first_name
                    user_last_name = obj.last_name
                });
                let li = CreateHtmlForUserTable(false, 'topic')
                Selectors.NotAccessUsersListForOneSubTopic.appendChild(li)
            })
        }

    } else {
        await getAllUsersForOneTopic(Selectors.curr_topic)
    }
}

async function getSharedUsersSearchboxSubject() {
    let text = document.getElementById('search-shared-for-subject').value
    if (text) {
        let url = (window.location.origin + '/files/api/access/searchbox/subject/' + Selectors.curr_subject + "/" + "?text=" + text + "&access=1"
        )
        let response = await fetch(url);
        if (response.ok) {
            let users = await response.json();
            Selectors.AccessUsersListForSubject.innerHTML = ''
            users.forEach(obj => {
                Object.entries(obj).forEach(([key, value]) => {
                    user_id = obj.id
                    user_first_name = obj.first_name
                    user_last_name = obj.last_name
                });

                let li = CreateHtmlForUserTable(true, 'subject')
                Selectors.AccessUsersListForSubject.appendChild(li)
            })
        }

    } else {

        await getUsersSubject(Selectors.curr_subject)
    }
}

async function getNotSharedUsersSearchBoxSubject() {
    let text = document.getElementById('search-sharing-for-subject').value
    if (text) {
        let url = (window.location.origin + '/files/api/access/searchbox/subject/' + Selectors.curr_subject + "/" + "?text=" + text + "&access=0"
        )
        let response = await fetch(url);
        if (response.ok) {
            let users = await response.json();
            Selectors.NotAccessUsersListForSubject.innerHTML = ''

            users.forEach(obj => {
                Object.entries(obj).forEach(([key, value]) => {
                    user_id = obj.id
                    user_first_name = obj.first_name
                    user_last_name = obj.last_name
                });

                let li = CreateHtmlForUserTable(false, 'subject')

                Selectors.NotAccessUsersListForSubject.appendChild(li)
            })
        }
    } else {
        await getUsersSubject(Selectors.curr_subject)
    }
};