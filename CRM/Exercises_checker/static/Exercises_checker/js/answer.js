let menuItems = document.querySelectorAll(".li-item"),
    sidebar = document.querySelector(".sidebar"),
    handler = document.querySelector(".devs-handler"),
    devmentorsCRM = document.querySelector(".mentors-top"),
    menuFooter = document.querySelector(".menu-footer-content"),
    hints = document.querySelectorAll(".hint"),
    counters = document.querySelector(".list-counter"),
    lines = document.querySelectorAll(".code-line"),
    solution = document.querySelector(".solution"),
    comment = document.querySelector(".only-comment"),
    outputTitle = document.querySelector(".output-title"),
    output = document.querySelector(".output-result");

// const changeAttribute = (item, property) => item.setAttribute('style', property);
const checkIfShort = () => sidebar.clientWidth < 56;

// const showLessMenu = () => menuItems.forEach(item => item.style.display = "none"),
// showMoreMenu = () => menuItems.forEach(item => item.style.display = "inline");

// const dontShowLogo = () => changeAttribute(devmentorsCRM, 'display: none'),
//     showLogo = () => changeAttribute(devmentorsCRM, 'display: inline');

// const showLess = () => {
//     changeAttribute(menuFooter, 'display: none')
//     menuItems.forEach(item => item.style.display = "none")
//     changeAttribute(devmentorsCRM, 'display: none')
// }

// const showMore = () => {
//     changeAttribute(menuFooter, 'display: block')
//     menuItems.forEach(item => item.style.display = "inline")
//     changeAttribute(devmentorsCRM, 'display: inline')
// }

// handler.addEventListener('click', () => {
//     if (!checkIfShort()) {
//         sidebar.setAttribute('style', 'width: 55px')
//         showLess()
//     } else {
//         sidebar.setAttribute('style', 'width: 390px')
//         setTimeout(() => {
//             showMore()
//         }, 100)
//     }
// })

hints.forEach(hint => {
    hint.addEventListener("click", () => {

        if (hint.querySelector(".hint-desc").style.display === "inline") {
            hint.querySelector(".hint-desc").style.display = "none"
        } else {
            hint.querySelector(".hint-desc").style.display = "inline"
        }
    })
})

// comment.addEventListener('click', () => {
//     comment.innerHTML = ""
// })

// document.querySelector(".run").addEventListener('click', () => {
//     outputTitle.innerHTML = '';
//     output.innerHTML = document.querySelector(".code-content").innerText;
// })


// if (document.body.clientWidth >= 700) {
//     showLess()
// }

window.addEventListener('resize', () => {
    if (document.body.clientWidth >= 700) {
        showLess()
        sidebar.setAttribute('style', 'width: 55px')
    }
})

