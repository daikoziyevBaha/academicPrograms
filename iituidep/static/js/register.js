
const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");

const firstNameField = document.querySelector("#firstNameField");
const firstNameFeedBackArea = document.querySelector(".firstNameFeedBackArea");

const lastNameField = document.querySelector("#lastNameField");
const lastNameFeedBackArea = document.querySelector(".lastNameFeedBackArea");

const passwordField = document.querySelector("#passwordField");
const confirmPassordField = document.querySelector("#confirmPasswordField")

const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector("#submitBtn");

console.log(submitBtn)

const handleToggleInput = (e) => {
  if (showPasswordToggle.textContent === "Показать") {
    showPasswordToggle.textContent = "Скрыть";
    passwordField.setAttribute("type", "text");
    confirmPassordField.setAttribute("type", "text");
  } else {
    showPasswordToggle.textContent = "Показать";
    passwordField.setAttribute("type", "password");
    confirmPassordField.setAttribute("type", "password")
  }
};

showPasswordToggle.addEventListener("click", handleToggleInput);

firstNameField.addEventListener("keyup", (e) => {
  const firstNameVal = e.target.value;

  firstNameField.classList.remove("is-invalid");
  firstNameFeedBackArea.style.display = "none";

  if (firstNameVal.length > 0) {
      fetch("/authentication/validate-first-name", {
      body: JSON.stringify({ first_name: firstNameVal }),
      method: "POST",
    })
        .then((res) => res.json()).then((data) => {
        if (data.first_name_error) {
          submitBtn.disabled = true;
          submitBtn.style.cursor = "not-allowed"
          firstNameField.classList.add("is-invalid");
          firstNameFeedBackArea.style.display = "block";
          firstNameFeedBackArea.innerHTML = `<p>${data.first_name_error}</p>`;
        } else {
          submitBtn.removeAttribute("disabled");
          submitBtn.style.cursor = "pointer";
        }
      });
  }
});

lastNameField.addEventListener("keyup", (e) => {
  const lastNameVal = e.target.value;
  lastNameField.classList.remove("is-invalid");
  lastNameFeedBackArea.style.display = "none";

  if (lastNameVal.length > 0) {
      fetch("/authentication/validate-last-name", {
      body: JSON.stringify({ last_name: lastNameVal }),
      method: "POST",
    })
        .then((res) => res.json()).then((data) => {
        if (data.last_name_error) {
          submitBtn.disabled = true;
          submitBtn.style.cursor = "not-allowed"
          lastNameField.classList.add("is-invalid");
          lastNameFeedBackArea.style.display = "block";
          lastNameFeedBackArea.innerHTML = `<p>${data.last_name_error}</p>`;
        } else {
          submitBtn.removeAttribute("disabled");
          submitBtn.style.cursor = "pointer";
        }
      });
  }
});

emailField.addEventListener("keyup", (e) => {
  const emailVal = e.target.value;

  emailField.classList.remove("is-invalid");
  emailFeedBackArea.style.display = "none";

  if (emailVal.length > 0) {
      fetch("/authentication/validate-email", {
      body: JSON.stringify({ email: emailVal }),
      method: "POST",
    })
        .then((res) => res.json()).then((data) => {
        if (data.email_error) {
          submitBtn.disabled = true;
          submitBtn.style.cursor = "not-allowed"
          emailField.classList.add("is-invalid");
          emailFeedBackArea.style.display = "block";
          emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
        } else {
          submitBtn.removeAttribute("disabled");
          submitBtn.style.cursor = "pointer";
        }
      });
  }
});


