const comment = document.querySelector(".only-comment"),
    outputTitle = document.querySelector(".output-title"),
    output = document.querySelector(".output-result"),
    buttons = document.querySelectorAll(".btn"),
    eye = document.querySelector(".eye"),
    blur = document.querySelector(".test-and-hints"),
    codeContent = document.querySelector(".code-content"),
    refresh = document.querySelector(".refresh"),
    submit = document.querySelector(".submit"),
    stat = document.querySelector(".status"),
    check = document.querySelector(".final-status-check"),
    failed = document.querySelector(".final-status-failed");

const test1check = document.querySelector(".test1-check"),
    test1failed = document.querySelector(".test1-failed"),
    test2check = document.querySelector(".test2-check"),
    test2failed = document.querySelector(".test2-failed"),
    test3check = document.querySelector(".test3-check"),
    test3failed = document.querySelector(".test3-failed");

//          Czy student zaliczył poszczególne testy?

let testObject = {
    "test1": false,
    "test2": true,
    "test3": true
}


const testsResult = Object.values(testObject)

//          Gdy wszystkie testy przeszły:
let finalResult = testsResult.every(Boolean)


const codeOnStart =
`<div class="code-line">function testFunc (array, sequence) {</div>
<div class="code-line only-comment"> <span class="c-comm">// Write your code
        here.</span>
</div>
<div class="code-line">}</div>

<div class="code-line readonly" readonly="true">exports. isValidSubsequence = isValidSubsequence;
</div>`

const changeAttribute = (item, property) => item.setAttribute('style', property);
const checkIfShort = () => sidebar.clientWidth < 56;

const changeStatus = (check, fail, bool) => {
    if(bool) {
        check.setAttribute("style", "display: inline")
        fail.setAttribute("style", "display: none")
    } else {
        fail.setAttribute("style", "display: inline")
        check.setAttribute("style", "display: none")
    }
}

// comment.addEventListener('click', () => comment.innerHTML = "")

document.querySelector(".run").addEventListener('click', () => {
    // const datas = document.querySelector(".code-content").innerText;
    submit.disabled = false;
    changeStatus(check, failed, finalResult)
    sendToComputing();


    for([test, testBool] of Object.entries(testObject)) {
        changeStatus(
            document.querySelector(`.${test}-check`),
            document.querySelector(`.${test}-failed`),
            testBool)
    }

    })

// })

buttons.forEach( element => {
    element.addEventListener('click', () => {
        element.querySelector(".arrow").classList.toggle("arrow-toggled")

    })
})

eye.addEventListener('click', () => {
    eye.classList.toggle("eye-active");
    blur.classList.toggle("blured")
})

// refresh.addEventListener('click', () => codeContent.innerHTML = codeOnStart)

submit.addEventListener('click', () => stat.classList.toggle("status-active"))
