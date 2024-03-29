class QuantityHandler {

    static doneExercises = document.getElementsByClassName("done-tasks")[0]
    static allExercises = document.getElementsByClassName("all-tasks")[0]
    static wholeProgressInfo = document.getElementsByClassName("student-info-progress p-3 mb-5")[0]
    static exerciseTable = document.getElementsByClassName("tab-content")[0]
    static doneEasyExercisesQuantity = document.getElementsByClassName("done-easy")[0]
    static easyExercisesQuantity = document.getElementsByClassName("total-easy")[0]
    static doneMediumExercisesQuantity = document.getElementsByClassName("done-medium")[0]
    static mediumExercisesQuantity = document.getElementsByClassName("total-medium")[0]
    static doneHardExercisesQuantity = document.getElementsByClassName("done-hard")[0]
    static hardExercisesQuantity = document.getElementsByClassName("total-hard")[0]

    static handleQuantity(quantity) {
        QuantityHandler.doneExercises.textContent = quantity.done_exercises_quantity
        QuantityHandler.allExercises.textContent = quantity.all_exercises_quantity
        QuantityHandler.easyExercisesQuantity.textContent = quantity.easy_exercises_quantity
        QuantityHandler.doneEasyExercisesQuantity.textContent = quantity.done_easy_exercises_quantity
        QuantityHandler.doneMediumExercisesQuantity.textContent = quantity.done_medium_exercises_quantity
        QuantityHandler.mediumExercisesQuantity.textContent = quantity.medium_exercises_quantity
        QuantityHandler.doneHardExercisesQuantity.textContent = quantity.done_hard_exercises_quantity
        QuantityHandler.hardExercisesQuantity.textContent = quantity.hard_exercises_quantity
    }

}


class ExercisesHandler {
    static exercisesListEasy = document.getElementsByClassName("tasks-list-box tasks-list-box-easy")[0]
    static exercisesLisMedium = document.getElementsByClassName("tasks-list-box tasks-list-box-medium")[0]
    static exercisesLisHard = document.getElementsByClassName("tasks-list-box tasks-list-box-hard")[0]

    static colorHtmlDict = {
        'easy': `<div class="level-color level-color-easy"></div>`,
        'medium': `<div class="level-color level-color-medium"></div>`,
        'hard': `<div class="level-color level-color-hard"></div>`
    }

    static exercisesListDict = {
        'easy': ExercisesHandler.exercisesListEasy,
        'medium': ExercisesHandler.exercisesLisMedium,
        'hard': ExercisesHandler.exercisesLisHard
    }

    static cleanExercisesListHtml() {
        for (let key in ExercisesHandler.exercisesListDict) {
            ExercisesHandler.exercisesListDict[key].innerHTML = ""
        }
    }

    static createExerciseHtml(exercise) {
        return `<a class="go-to-checker" href="${window.location.href}${exercise.id}/">
                    <div class="complete-box"></div>
                    <div class="task-name">
                        <span>${exercise.name}</span>
                    </div>
                </a>`
    }


    static handleAllExercises(exercises) {
        const keys = Object.keys(exercises);
        keys.forEach((key, index) => {
            this.handleEasyExercises(key, exercises[key]);
        });
    }

    static handleEasyExercises(exercises_type, exercises) {
        exercises.forEach(exercise => {
            Object.entries(exercise).forEach(([key, value]) => {
            });
            let main_div = document.createElement('div');
            main_div.className = "task-box mb-2";
            main_div.innerHTML = (ExercisesHandler.createExerciseHtml(exercise));
            let complete_box = main_div.getElementsByClassName("complete-box")[0]
            complete_box.innerHTML = (ExercisesHandler.handleStatusDiv(exercise.done))
            this.handleTypeDiv(main_div, exercises_type)
            this.segregateExercisesTable(exercises_type, main_div);

        });
    }

    static handleStatusDiv(status) {
        if (status) {
            return `<div class="complete-circle complete"></div>`
        } else {
            return `<div class="complete-circle"></div>`
        }
    }

    static handleTypeDiv(main_div, exercises_type) {
        let colour_div = document.createElement('div')
        let go_to_checker = main_div.getElementsByClassName("go-to-checker")[0]
        colour_div.innerHTML = ExercisesHandler.colorHtmlDict[exercises_type]
        go_to_checker.appendChild(colour_div)

    }

    static segregateExercisesTable(exercises_type, main_div) {
        ExercisesHandler.exercisesListDict[exercises_type].appendChild(main_div)
    }
}

function getExercises(path_id){
    ExercisesHandler.cleanExercisesListHtml()
    getJson('/exercises/api/access/exercises/' + path_id)
        .then(response =>{
            QuantityHandler.handleQuantity(response.quantity);
            ExercisesHandler.handleAllExercises(response.exercises);
            QuantityHandler.wholeProgressInfo.style.visibility = "visible"
            QuantityHandler.exerciseTable.style.visibility = "visible"
            updateProgressBarr(response.quantity.done_exercises_quantity, response.quantity.all_exercises_quantity)
        })
}

document.addEventListener('DOMContentLoaded', function () {
    let languages = document.querySelectorAll('.nav-link:not(.disabled)')
    if(languages.length > 0){
        languages[0].classList.add('active');
        let languageId  = languages[0].id.split('-').pop();
        getExercises(languageId)
    }
}, false);

function updateProgressBarr(doneTasks, allTasks){
    let progress = parseInt((doneTasks / allTasks) * 100)
    document.getElementsByClassName('progress-bar')[0].style.width = `${progress}%`
}