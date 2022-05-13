document.addEventListener('DOMContentLoaded', function () {

}, false);


class FilesHandler {
    selectors = {
        themeName: document.querySelectorAll('a.theme-name.available'),
        themeDetails: document.querySelector('.themes-details'),
        fileDetails: this.selectors.themeDetails.children,
        tittle: this.selectors.fileDetails.namedItem('tittle'),
        filesContainer: this.selectors.fileDetails.namedItem('container'),
        description: this.selectors.fileDetails.namedItem('description'),
        filesList: this.selectors.filesContainer.children.namedItem('filesListContainer').children.namedItem('filesList'),
        backBtn: document.querySelector('.back-btn'),
        AccessUsersListForOneSubTopic: document.getElementsByClassName("shared-for-student-list")[0].children.namedItem("shared_for_one"),
        NotAccessUsersListForOneSubTopic: document.getElementsByClassName("sharing-student-list")[0].children.namedItem("share_for_one"),
        ThemeNameForOne: document.getElementsByClassName("theme-name").namedItem('tittle_modal_for_one'),
        ThemeNameForSubject: document.getElementsByClassName("category-name").namedItem("tittle_modal_for_subject"),
        AccessUsersListForSubject: document.getElementsByClassName("shared-for-student-list")[1].children.namedItem("shared_for_all"),
        NotAccessUsersListForSubject: document.getElementsByClassName("sharing-student-list")[1].children.namedItem("share_for_all"),
        searchShared: document.querySelector('.search-shared-for'),
        searchSharing: document.querySelector('.search-sharing'),
        liSharing: document.querySelectorAll('.sharing-student-name'),
        liShared: document.querySelectorAll('.shared-for-student-name'),
        user_id: '',
        user_first_name: '',
        user_last_name: '',
        access: '',
        curr_topic: "",
        curr_subject: "",
        csrftoken: getCookie('csrftoken'),
    }

    static apiUrls = {}

    searchEngine = (selector, text) => {
        selector.forEach(el => {
            if (el.textContent.toLowerCase().indexOf(text) !== -1) {
                el.style.display = 'block'
            } else {
                el.style.display = 'none'
            }
        })
    }


    toggleDetails = () => {
        if (Selectors.themeDetails.style.display === "none") {
            Selectors.themeDetails.style.display = "block";
        } else {
            Selectors.themeDetails.style.display = "none";
        }
    }



}

let  filesHandler = new  FilesHandler()


filesHandler.selectors.addEventListener('click', filesHandler.toggleDetails);
filesHandler.selectors.themeName.forEach(name => name.addEventListener('click', toggleDetails));
filesHandler.selectors.searchShared.addEventListener('keyup', () => {
    const text = this.target.value.toLowerCase();
    filesHandler.searchEngine(this.selectors.liShared, text)
});
