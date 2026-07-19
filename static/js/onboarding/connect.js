// ===============================
// CampusForge Connect Accounts
// ===============================

const connectButtons = document.querySelectorAll(".connect-btn");
const syncButtons = document.querySelectorAll(".sync-btn");

const progressBar = document.querySelector(".progress");
const completionText = document.querySelector(".completion small");

let connectedAccounts = document.querySelectorAll(".account.connected").length;
const totalAccounts = document.querySelectorAll(".account").length;

// ===============================
// Toast Notification
// ===============================

function showToast(message){

    const toast = document.createElement("div");

    toast.className = "toast";

    toast.innerHTML = `
        <i class="fa-solid fa-circle-check"></i>
        ${message}
    `;

    document.body.appendChild(toast);

    setTimeout(()=>{

        toast.classList.add("show");

    },100);

    setTimeout(()=>{

        toast.classList.remove("show");

        setTimeout(()=>{

            toast.remove();

        },300);

    },3000);

}

// ===============================
// Update Progress
// ===============================

function updateProgress(){

    const percentage = Math.round((connectedAccounts / totalAccounts) * 20 + 80);

    progressBar.style.width = percentage + "%";

    completionText.textContent = percentage + "% Completed";

}

// ===============================
// Connect Account
// ===============================

connectButtons.forEach(button=>{

    button.addEventListener("click",()=>{

        const card = button.closest(".account");

        if(card.classList.contains("connected")) return;

        card.classList.add("loading");

        button.innerHTML = `
            <i class="fa-solid fa-spinner"></i>
            Connecting...
        `;

        setTimeout(()=>{

            card.classList.remove("loading");

            card.classList.add("connected");
            card.classList.add("success");

            connectedAccounts++;

            updateProgress();

            const platform = card.querySelector("h2").textContent;

            const badge = card.querySelector(".status-badge");

            badge.className = "status-badge connected-badge";

            badge.innerHTML = `
                <i class="fa-solid fa-circle-check"></i>
                Connected
            `;

            const preview = card.querySelector(".preview");

            if(preview){

                preview.outerHTML = `

                <div class="stats">

                    <div>

                        <span>Score</span>

                        <strong>${Math.floor(Math.random()*500)+100}</strong>

                    </div>

                    <div>

                        <span>Badges</span>

                        <strong>${Math.floor(Math.random()*20)+1}</strong>

                    </div>

                    <div>

                        <span>Rank</span>

                        <strong>#${Math.floor(Math.random()*900)+100}</strong>

                    </div>

                </div>

                <div class="sync">

                    <span>Last Sync</span>

                    <strong>Just now</strong>

                </div>

                `;

            }

            button.className = "sync-btn";

            button.innerHTML = `
                <i class="fa-solid fa-rotate"></i>
                Sync Now
            `;

            showToast(platform + " connected successfully!");

            attachSync(button);

        },2000);

    });

});

// ===============================
// Sync Function
// ===============================

function attachSync(button){

    button.addEventListener("click",()=>{

        const card = button.closest(".account");

        const syncText = card.querySelector(".sync strong");

        button.disabled = true;

        button.innerHTML = `
            <i class="fa-solid fa-spinner"></i>
            Syncing...
        `;

        button.classList.add("loading");

        setTimeout(()=>{

            syncText.textContent = "Just now";

            button.disabled = false;

            button.classList.remove("loading");

            button.innerHTML = `
                <i class="fa-solid fa-rotate"></i>
                Sync Now
            `;

            const platform = card.querySelector("h2").textContent;

            showToast(platform + " synced successfully!");

        },1500);

    });

}

// Existing Sync Buttons

syncButtons.forEach(btn=>{

    attachSync(btn);

});

// Initial Progress

updateProgress();