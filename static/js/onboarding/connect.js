// ===============================
// CampusForge Connect Accounts
// ===============================


// ===============================
// DOM ELEMENTS
// ===============================

const connectButtons = document.querySelectorAll("button.connect-btn");

const syncButtons = document.querySelectorAll(".sync-btn");

const progressBar = document.querySelector(".progress");

const completionText =
    document.querySelector(".completion small");

let connectedAccounts =
    document.querySelectorAll(".account.connected").length;

const totalAccounts =
    document.querySelectorAll(".account").length;


// ===============================
// CONNECT MODAL ELEMENTS
// ===============================

const modal =
    document.getElementById("connectModal");

const closeModal =
    document.getElementById("closeModal");

const modalPlatform =
    document.getElementById("modalPlatform");

const modalPlatformInput =
    document.getElementById("modalPlatformInput");

const platformUsername =
    document.getElementById("platformUsername");


// ===============================
// TOAST NOTIFICATION
// ===============================

function showToast(message) {

    const toast = document.createElement("div");

    toast.className = "toast";

    toast.innerHTML = `
        <i class="fa-solid fa-circle-check"></i>
        ${message}
    `;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.classList.add("show");
    }, 100);

    setTimeout(() => {

        toast.classList.remove("show");

        setTimeout(() => {
            toast.remove();
        }, 300);

    }, 3000);
}


// ===============================
// UPDATE PROGRESS
// ===============================

function updateProgress() {

    const percentage =
        Math.round(
            (connectedAccounts / totalAccounts) * 20 + 80
        );

    if (progressBar) {
        progressBar.style.width =
            percentage + "%";
    }

    if (completionText) {
        completionText.textContent =
            percentage + "% Completed";
    }
}


// ===============================
// OPEN CONNECT MODAL
// ===============================

connectButtons.forEach(button => {

    button.addEventListener("click", () => {

        const platform =
            button.dataset.platform;

        // Set platform name in modal
        modalPlatform.textContent =
            platform;

        // Set hidden input value
        modalPlatformInput.value =
            platform;

        // Clear previous username
        platformUsername.value = "";

        // Open modal
        modal.style.display = "flex";

        // Focus username field
        platformUsername.focus();

    });

});


// ===============================
// CLOSE MODAL
// ===============================

closeModal.addEventListener("click", () => {

    modal.style.display = "none";

});


// ===============================
// CLOSE MODAL
// WHEN CLICKING OUTSIDE
// ===============================

modal.addEventListener("click", (event) => {

    if (event.target === modal) {

        modal.style.display = "none";

    }

});


// ===============================
// CLOSE MODAL WITH ESC KEY
// ===============================

document.addEventListener("keydown", (event) => {

    if (
        event.key === "Escape" &&
        modal.style.display === "flex"
    ) {

        modal.style.display = "none";

    }

});


// ===============================
// SYNC FUNCTION
// ===============================

function attachSync(button) {

    button.addEventListener("click", () => {

        const card =
            button.closest(".account");

        const syncText =
            card.querySelector(".sync strong");

        button.disabled = true;

        button.innerHTML = `
            <i class="fa-solid fa-spinner"></i>
            Syncing...
        `;

        button.classList.add("loading");


        setTimeout(() => {

            syncText.textContent =
                "Just now";

            button.disabled = false;

            button.classList.remove("loading");

            button.innerHTML = `
                <i class="fa-solid fa-rotate"></i>
                Sync Now
            `;

            const platform =
                card.querySelector("h2").textContent;

            showToast(
                platform +
                " synced successfully!"
            );

        }, 1500);

    });

}


// ===============================
// EXISTING SYNC BUTTONS
// ===============================

syncButtons.forEach(button => {

    attachSync(button);

});


// ===============================
// INITIAL PROGRESS
// ===============================

updateProgress();