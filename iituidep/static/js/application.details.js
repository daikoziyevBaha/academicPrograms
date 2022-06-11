const submitBtn = document.querySelector('#submitBtn')
submitBtn.style.cursor = "not-allowed";
const authorityRules = document.querySelector("#authorityRules");

var exchangeInfo = document.querySelector("#exchangeinfo_status");
var personalInfo = document.querySelector("#personal_status");
var curriculumInfo = document.querySelector("#curriculum_status");
var documentsInfo = document.querySelector("#documents_status");

// console.log(exchangeInfo.textContent, personalInfo.textContent, curriculumInfo.textContent, documentsInfo.textContent);

// document.addEventListener("DOMContentLoaded", function() {
    
//     if (exchangeInfo.textContent === "Заполнен" && documentsInfo.textContent === "Заполнен" && personalInfo.textContent === "Заполнен" && curriculumInfo.textContent === "Заполнен"){
//         console.log("SUBMIT")
//         submitBtn.type = "submit"
//     }
// });

authorityRules.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
        submitBtn.removeAttribute("disabled");
        submitBtn.style.cursor = "pointer";
    } else {
        submitBtn.disabled = true;
        submitBtn.style.cursor = "not-allowed";
    }
  });

// submitBtn.addEventListener("click", function() {
//      if (exchangeInfo.textContent === "Заполнен" && documentsInfo.textContent === "Заполнен"  && personalInfo.textContent === "Заполнен" && curriculumInfo.textContent === "Заполнен"){
//          console.log('Заполнены оба поля');
//      }
//      else {
//          $("#modal").modal("show");
//      }
// });

document.querySelector("#btnHide").addEventListener("click", function(){
    $("#modal").modal("hide");
});


