// let Selectors = { "code_field" : document.getElementById("code-form").elements['editor'],
//                     // "info_header" : document.getElementById('info')

// }

// document.getElementById('send-button').addEventListener('click',  function(){
//      sendToComputing();
// })

async function saveCodeToDB(result){
    let data = {}

    let editor = ace.edit('editor')
    data.code = editor.getValue()
    data.done = result.is_all_tests_passed
    let url = `${getBaseUrl('/exercises/api/access/exercises/code/')}${exercise_status_id}`
    config = {
            method: 'PATCH',
            headers: {
            'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie("csrftoken")
            },
            body: JSON.stringify(data)
        }
    response = await fetch(url, config)
    if (response.ok){
        if (result.done){
            console.log("Congratulations! You've passed all the test")
        }else{
            let error = result.error
        }
    }
}

async function getToken(){
    let token_url = `${window.location.origin}/exercises/api/token/`
    let token_response = await (await fetch(token_url)).json();
    return token_response.access
}

async function sendToComputing() {
    let data = {}
    // TODO check computing host
    // let computing_url =  "http://computing:8002/"
    let computing_url = "http://localhost:8002/"
    let token = await getToken()
    // data.code = Selectors['code_field'].value
    let editor =ace.edit('editor')
    data.code = editor.getValue()
    // console.log(editor.getValue())
    data.language = language
    data.name = slug_name
    config = {
        method: 'POST',
        headers: {
        'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': token,
            'X-CSRFToken': getCookie("csrftoken")
        },
        body: JSON.stringify(data)
    }

    let computing_response = await fetch(computing_url, config)
    let body = await computing_response.json()
    if (computing_response.ok){
        // console.log("response ok ", body.task_id)
        getStatus(body.task_id)
    }
}


function getStatus(taskID){
    let url = `http://localhost:8002/tasks/${taskID}/`;
    fetch(url)
    .then(res => res.json())
        .then(data => {
            // console.log(taskID," ", data)
            const taskStatus = data.task_status;
            const taskResult = data.task_result;
            if (taskStatus === 'FAILURE') {
                console.log('FAILURE');
                return false
            }else if(taskStatus === 'SUCCESS'){
                console.log('DUPA', data.task_result);
                if (data.task_result.error_message)
                    return false
                saveCodeToDB(data.task_result);
                return true
            }
            setTimeout(function (){
                getStatus(taskID);
            }, 10)
        })
}
