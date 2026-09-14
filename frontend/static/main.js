fetch("http://127.0.0.1:5000/api/dashboard")
.then(response => response.json())
.then(data =>{
    document.getElementById("securityScore").textContent =
       data.security_score + "%" ;
    document.getElementById("passwordChecks").textContent =
       data.password_checked;
    document.getElementById("emailsScanned").textContent =
       data.emails_scanned;
    document.getElementById("urlsChecked").textContent =
       data.urls_checked;
    document.getElementById("weakPassword").textContent =
       data.weak_password;
    document.getElementById("phishingEmails").textContent =
       data.phishing_emails;
    document.getElementById("unsafeUrls").textContent =
       data.unsafe_urls;
})
.catch(error =>{
    console.error("Error:", error);
});




const errorMessage = document.getElementById("error-message");

if (errorMessage && errorMessage.textContent.trim() !== "") {
    errorMessage.style.color = "red";

    setTimeout(() => {
        errorMessage.style.display = "none";
    }, 3000);
}

//dashboard, saving password, email and url
function goToAssessment(type){

    localStorage.setItem("selectedAssessment", type);

    window.location.href = "/assessment";
}





// Password Analysis


async function check_password() {
    const password =
        document.getElementById("passwordInput").value;

    const response = await fetch("/analyze-password", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            password: password
        })
    });

    const data = await response.json();

    localStorage.setItem("passwordScore", data.score);

    localStorage.setItem(
    "passwordIssues",
    JSON.stringify(data.issues)
);

localStorage.setItem(
    "passwordLevel",
    data.level
);
    window.location.href = "/results";
}


// Email Analysis


async function analyzeEmail() {
    // email code
}


// URL Analysis


async function analyzeURL() {
    // url code
}


//Analyze Email
async function analyzeEmail() {

    const email =
        document.getElementById("emailInput").value;

    const response = await fetch("/analyze-email", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email
        })
    });

    const data = await response.json();

    localStorage.setItem(
        "emailScore",
        data.score
    );

    localStorage.setItem(
        "emailIssues",
        JSON.stringify(data.issues)
    );

    window.location.href = "/results";
}

//Analyze URL 

async function analyzeURL() {

    const url =
        document.getElementById("urlInput").value;

    const response = await fetch("/analyze-url", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            url: url
        })
    });

    const data = await response.json();

    localStorage.setItem(
        "urlScore",
        data.score
    );

    localStorage.setItem(
        "urlIssues",
        JSON.stringify(data.issues)
    );

    window.location.href = "/results";
}


//assessment_buttons 

document.addEventListener("DOMContentLoaded", () => {

    const passwordBtn = document.getElementById("passwordBtn");
    const emailBtn = document.getElementById("emailBtn");
    const urlBtn = document.getElementById("urlBtn");

    if (passwordBtn) {
        passwordBtn.addEventListener("click", check_password);
    }

    if (emailBtn) {
        emailBtn.addEventListener("click", analyzeEmail);
    }

    if (urlBtn) {
        urlBtn.addEventListener("click", analyzeURL);
    }

    displayEmailIssues();
    displayURLIssues();
    displayPasswordIssues();

});


//display URL issues on result page 

function displayURLIssues() {

    const issues =
        JSON.parse(localStorage.getItem("urlIssues")) || [];

    const issueList =
        document.getElementById("urlIssues");

    if (!issueList) return;

    issueList.innerHTML = "";

    issues.forEach(issue => {

        const li = document.createElement("li");

        li.textContent = issue;

        issueList.appendChild(li);

    });
}

//display Email Issues

function displayEmailIssues() {

    const issues =
        JSON.parse(localStorage.getItem("emailIssues")) || [];

    const issueList =
        document.getElementById("emailIssues");

    if (!issueList) return;

    issueList.innerHTML = "";

    issues.forEach(issue => {

        const li = document.createElement("li");
        li.textContent = issue;
        issueList.appendChild(li);

    });
}

//password displayer

function displayPasswordIssues() {

    const issues =
        JSON.parse(
            localStorage.getItem("passwordIssues")
        ) || [];

    const issueList =
        document.getElementById("passwordIssues");

    if (!issueList) return;

    issueList.innerHTML = "";

    issues.forEach(issue => {

        const li =
            document.createElement("li");

        li.textContent = issue;

        issueList.appendChild(li);

    });

}