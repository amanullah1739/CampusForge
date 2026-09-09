function selectSignupType(type) {

    const buttons = document.querySelectorAll(".signup-type-btn");
    const signupType = document.getElementById("signup_type");

    buttons.forEach(button => {
        button.classList.remove("active");
    });

    if (type === "student") {
        buttons[0].classList.add("active");
    } else {
        buttons[1].classList.add("active");
    }

    signupType.value = type;
}