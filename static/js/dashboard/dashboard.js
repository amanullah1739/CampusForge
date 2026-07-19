/* ==========================================
        CAMPUSFORGE DASHBOARD
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    animateCounters();

    animateProgressBars();

    welcomeAnimation();

});


/* ==========================================
        ANIMATED COUNTERS
========================================== */

function animateCounters(){

    const counters = document.querySelectorAll(".stat-card h3");

    counters.forEach(counter=>{

        let target = parseInt(counter.innerText.replace(/\D/g,'')) || 0;

        let count = 0;

        let increment = Math.ceil(target / 80);

        let interval = setInterval(()=>{

            count += increment;

            if(count >= target){

                count = target;

                clearInterval(interval);

            }

            if(counter.innerText.includes("#")){

                counter.innerText = "#" + count;

            }

            else if(counter.innerText.includes("Day")){

                counter.innerText = count;

            }

            else{

                counter.innerText = count;

            }

        },20);

    });

}


/* ==========================================
        PROGRESS BAR ANIMATION
========================================== */

function animateProgressBars(){

    const bars = document.querySelectorAll(".progress-fill,.xp-fill,.skill-bar div");

    bars.forEach(bar=>{

        const finalWidth = window.getComputedStyle(bar).width;

        bar.style.width = "0";

        setTimeout(()=>{

            bar.style.transition="width 1.8s ease";

            bar.style.width=finalWidth;

        },400);

    });

}


/* ==========================================
        HERO ANIMATION
========================================== */

function welcomeAnimation(){

    const hero=document.querySelector(".hero");

    hero.style.opacity="0";

    hero.style.transform="translateY(40px)";

    setTimeout(()=>{

        hero.style.transition="1s";

        hero.style.opacity="1";

        hero.style.transform="translateY(0)";

    },200);

}


/* ==========================================
        CARD HOVER EFFECT
========================================== */

const cards=document.querySelectorAll(".card");

cards.forEach(card=>{

    card.addEventListener("mousemove",(e)=>{

        const rect=card.getBoundingClientRect();

        const x=e.clientX-rect.left;

        const y=e.clientY-rect.top;

        card.style.background=`
        radial-gradient(circle at ${x}px ${y}px,
        rgba(108,99,255,.18),
        rgba(255,255,255,.05) 55%)`;

    });

    card.addEventListener("mouseleave",()=>{

        card.style.background="rgba(255,255,255,.05)";

    });

});


/* ==========================================
        LEVEL CIRCLE PULSE
========================================== */

const level=document.querySelector(".level-circle");

setInterval(()=>{

    level.animate([

        {transform:"scale(1)"},

        {transform:"scale(1.05)"},

        {transform:"scale(1)"}

    ],{

        duration:1400

    });

},3000);

/* ==========================================
        DARK MODE
========================================== */

const themeBtn=document.getElementById("themeToggle");

const body=document.body;

if(localStorage.getItem("theme")==="light"){

body.classList.add("light");

themeBtn.innerHTML='<i class="fa-solid fa-sun"></i>';

}

themeBtn.addEventListener("click",()=>{

body.classList.toggle("light");

if(body.classList.contains("light")){

themeBtn.innerHTML='<i class="fa-solid fa-sun"></i>';

localStorage.setItem("theme","light");

}

else{

themeBtn.innerHTML='<i class="fa-solid fa-moon"></i>';

localStorage.setItem("theme","dark");

}

});


/* ==========================================
        NOTIFICATIONS
========================================== */

const notifyBtn=document.getElementById("notificationBtn");

const panel=document.querySelector(".notification-panel");

notifyBtn.addEventListener("click",(e)=>{

e.stopPropagation();

panel.classList.toggle("show");

});

document.addEventListener("click",()=>{

panel.classList.remove("show");

});


/* ==========================================
        LIVE SEARCH
========================================== */

const search=document.querySelector(".search-box input");

search.addEventListener("keyup",()=>{

const value=search.value.toLowerCase();

document.querySelectorAll(".card").forEach(card=>{

const text=card.innerText.toLowerCase();

card.style.display=text.includes(value)?"block":"none";

});

});


/* ==========================================
        MOBILE SIDEBAR
========================================== */

const menu=document.querySelector(".menu-toggle");

const sidebar=document.querySelector(".sidebar");

menu.addEventListener("click",()=>{

sidebar.classList.toggle("active");

});

/* ==========================================
        XP SYSTEM
========================================== */

let xp = parseInt(localStorage.getItem("xp")) || 2380;

const xpText = document.querySelector(".xp-info strong");

const xpFill = document.querySelector(".xp-fill");

const toast = document.getElementById("toast");

const missions = document.querySelectorAll(".mission-list li");

missions.forEach((mission,index)=>{

    const checkbox = mission.querySelector("input");

    const saved = localStorage.getItem("mission"+index);

    if(saved==="true"){

        checkbox.checked=true;

        mission.classList.add("completed");

    }

    checkbox.addEventListener("change",()=>{

        if(checkbox.checked){

            mission.classList.add("completed");

            const reward=parseInt(mission.dataset.xp);

            xp += reward;

            updateXP();

            showToast("⭐ +" + reward + " XP Earned!");

            localStorage.setItem("mission"+index,true);

        }

        else{

            mission.classList.remove("completed");

            localStorage.removeItem("mission"+index);

        }

    });

});

function updateXP(){

    xpText.innerText=xp+" XP";

    const percent=(xp%3000)/30;

    xpFill.style.width=percent+"%";

    localStorage.setItem("xp",xp);
    checkLevel();

}

function showToast(message){

    toast.innerText=message;

    toast.classList.add("show");

    setTimeout(()=>{

        toast.classList.remove("show");

    },2500);

}

updateXP();

/* ==========================================
        ACHIEVEMENTS
========================================== */

const popup=document.getElementById("achievementPopup");

const popupText=document.getElementById("achievementText");

function unlockAchievement(text){

popupText.innerText=text;

popup.classList.add("show");

setTimeout(()=>{

popup.classList.remove("show");

},3500);

}

/* ==========================================
        LEVEL SYSTEM
========================================== */

let currentLevel=15;

function checkLevel(){

const level=document.querySelector(".level-circle h1");

if(xp>=3000){

currentLevel++;

xp=0;

level.innerText=currentLevel;

document.querySelector(".level-circle").classList.add("level-up");

showToast("🎉 LEVEL UP!");

unlockAchievement("Reached Level "+currentLevel);

setTimeout(()=>{

document.querySelector(".level-circle").classList.remove("level-up");

},900);

}

}

/* ==========================================
        STREAK
========================================== */

let streak=parseInt(localStorage.getItem("streak"))||18;

document.querySelector(".streak").innerHTML=

`🔥 ${streak} Day Streak`;

function increaseStreak(){

streak++;

localStorage.setItem("streak",streak);

document.querySelector(".streak").innerHTML=

`🔥 ${streak} Day Streak`;

}

/* ==========================================
        HEATMAP
========================================== */

const boxes=document.querySelectorAll(".box");

boxes.forEach(box=>{

box.addEventListener("mouseenter",()=>{

box.animate([

{

transform:"scale(1)"

},

{

transform:"scale(1.35)"

},

{

transform:"scale(1)"

}

],{

duration:300

});

});

});

/* ==========================================
        AI COACH
========================================== */

const tips=[

"Practice one Medium LeetCode problem today.",

"Push your latest project to GitHub.",

"Improve your LinkedIn profile this week.",

"Complete one Backend module today.",

"Review your DSA notes before sleeping.",

"Build a mini project this weekend.",

"Contribute to an open-source repository."

];

const coach=document.querySelector(".coach-message p");

setInterval(()=>{

const random=Math.floor(Math.random()*tips.length);

coach.innerText=tips[random];

},8000);

/* ==========================================
        PROFILE MENU
========================================== */

const profile=document.getElementById("profileMenu");

const dropdown=document.querySelector(".profile-dropdown");

profile.addEventListener("click",(e)=>{

e.stopPropagation();

dropdown.classList.toggle("show");

});

document.addEventListener("click",()=>{

dropdown.classList.remove("show");

});

/* ==========================================
        SETTINGS
========================================== */

const settings=document.querySelector(".profile-dropdown div:nth-child(2)");

const modal=document.getElementById("settingsModal");

const closeBtn=document.getElementById("closeSettings");

settings.addEventListener("click",()=>{

modal.classList.add("show");

});

closeBtn.addEventListener("click",()=>{

modal.classList.remove("show");

});

/* ==========================================
        BADGE SYSTEM
========================================== */

let badges=JSON.parse(localStorage.getItem("badges"))||[];

function earnBadge(name){

if(badges.includes(name)) return;

badges.push(name);

localStorage.setItem("badges",JSON.stringify(badges));

unlockAchievement("🏅 "+name);

}

/* ==========================================
        SMART NOTIFICATIONS
========================================== */

const smartNotifications=[

"🔥 Keep your streak alive today!",

"📈 Your XP increased this week.",

"🚀 Upload your latest project.",

"🏆 You're close to the Top 10 leaderboard.",

"💻 Solve today's coding challenge."

];

setInterval(()=>{

const random=Math.floor(Math.random()*smartNotifications.length);

showToast(smartNotifications[random]);

},60000);

/* ==========================================
        XP HISTORY
========================================== */

let history=JSON.parse(localStorage.getItem("xpHistory"))||[];

function saveXPHistory(){

history.push({

date:new Date().toLocaleDateString(),

xp:xp

});

localStorage.setItem("xpHistory",JSON.stringify(history));

}

/* ==========================================
        LOGOUT
========================================== */

document.querySelector(".logout-item").addEventListener("click",()=>{

if(confirm("Are you sure you want to logout?")){

localStorage.removeItem("theme");

location.reload();

}

});

/* ==========================================
        ANALYTICS
========================================== */

function analytics(){

console.log("Current XP:",xp);

console.log("Level:",currentLevel);

console.log("Badges:",badges.length);

console.log("History:",history);

}

analytics();