let Selectors = { "code_field" : document.getElementById("code-form").elements['code'],
                    "info_header" : document.getElementById('info')

}

document.getElementById('send-button').addEventListener('click',  function(){
     sendToComputing();
     saveCodeToDB();
})
    
async function saveCodeToDB(){
    let data = {}
    data.code = Selectors['code_field'].value
    let url = `${window.location.origin}/exercises/api/access/exercises/code/${exercise_status_id}`
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
    data.code = Selectors['code_field'].value
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
        
        // if(body.done === true){
        //     window.alert("OK!")

        // }
        // else if (body.done=== false){
        //     window.alert(`TEST PASSED:${body.test_passed}`)

        // }
            
        }

    // else{
    //         Selectors["info_header"].innerText = body.error

    // }

        }


function getStatus(taskID){
    // console.log(taskID)
    let url = `http://localhost:8002/tasks/${taskID}/`;
    // console.log(url)
    fetch(url)
    .then(res => res.json())
        .then(data => {
            // console.log(data);
            const taskStatus = data.task_status;
            const taskResult = data.task_result;
            // console.log(taskResult)
            if (taskStatus === 'FAILURE') {
                console.log('dupa');
                return false
            }else if(taskStatus === 'SUCCESS'){
                console.log(taskResult);
                return true
            }
            setTimeout(function (){
                // console.log(taskStatus);
                getStatus(taskID);
            }, 1000)
        })
}
    






