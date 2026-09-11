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