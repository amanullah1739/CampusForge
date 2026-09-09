function selectSignupType(type) {

    const buttons = document.querySelectorAll(".signup-type-btn");

    const signupType = document.getElementById("signup_type");

    const studentFields = document.getElementById("student-fields");

    const collegeField = document.getElementById("college-field");

    const submitButton = document.querySelector(
        'button[type="submit"]'
    );

    // Remove active state
    buttons.forEach(button => {
        button.classList.remove("active");
    });


    // =========================
    // STUDENT
    // =========================

    if (type === "student") {

        buttons[0].classList.add("active");

        signupType.value = "student";

        studentFields.style.display = "block";

        collegeField.style.display = "block";


        // Student fields required
        studentFields
            .querySelectorAll("input, select")
            .forEach(field => {
                field.required = true;
            });


        submitButton.textContent = "Create Student Account";
    }


    // =========================
    // ADMIN
    // =========================

    else {

        buttons[1].classList.add("active");

        signupType.value = "admin";

        studentFields.style.display = "none";

        collegeField.style.display = "block";


        // Student fields not required
        studentFields
            .querySelectorAll("input, select")
            .forEach(field => {
                field.required = false;
            });


        submitButton.textContent = "Create Admin Account";
    }
}