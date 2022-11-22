// let Selectors = { "code_field" : document.getElementById("code-form").elements['editor'],
//                     // "info_header" : document.getElementById('info')

// }

document.getElementById('send-button').addEventListener('click',  function(){
     sendToComputing();
})

async function saveCodeToDB(result){
    let data = {}
    // data.code = Selectors['code_field'].value
    // data.code = Selectors['code_field'].innerHTML
    // data.code = document.getElementById('editor').textContent
    let editor =ace.edit('editor')
    data.code = editor.getValue()
    console.log(editor.getValue())
    data.done = result.done
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
        // let myModal = document.getElementById('myModal');
        // var modal = bootstrap.Modal.getOrCreateInstance(myModal);
        // let modalBody = document.querySelector('#myModal .modal-body');
        let abc = document.getElementById('output-result')

        if (result.done){
            abc.textContent = "Congratulations! You've passed all the test"
            // modalBody.textContent = "Congratulations! You've passed all the test"
            // myModal.addEventListener('hide.bs.modal', function (event) {
            //     window.location.href = `${getBaseUrl('/exercises/')}`;
            //   })
        }else{
            abc.textContent = `You passed: ${result.test_passed} tests - Try again.`
            let error = result.error
            const textNode = document.createTextNode(error.error_message);
            abc.appendChild(textNode)
            // abc.insertAdjacentText("beforeend", '<p>' + error.error_message);


            // modalBody.textContent = `You passed: ${result.test_passed} tests - Try again.`
        }
        // modal.show(myModal)
    }

}

async function getToken(){
    let token_url = `${window.location.origin}/exercises/api/token/`
    let token_response = await (await fetch(token_url)).json();
    return token_response.access
}

async function sendToComputing() {
let data = {}
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
        getStatus(body.task_id)
    }
}


function getStatus(taskID){
    let url = `http://localhost:8002/tasks/${taskID}/`;
    fetch(url)
    .then(res => res.json())
        .then(data => {
            const taskStatus = data.task_status;
            const taskResult = data.task_result;
            console.log(data.task_result);
            if (taskStatus === 'FAILURE') {
                console.log('dupa');
                return false
            }else if(taskStatus === 'SUCCESS'){
                console.log('DUPA', data.task_result);
                saveCodeToDB(data.task_result)
                return true
            }
            setTimeout(function (){
                getStatus(taskID);
            }, 100)
        })
}







