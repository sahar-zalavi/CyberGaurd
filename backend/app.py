from flask import Flask, render_template, redirect, url_for, request, jsonify, session, flash # pyright: ignore[reportMissingImports]
from flask_mysqldb import MySQL  # pyright: ignore[reportMissingImports]
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static",
)
app.config["SECRET_KEY"] = "super-secret-key"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Solin1393@"
app.config["MYSQL_DB"] = "security_app"

CORS(app)
mysql = MySQL(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():

    full_name = session.get("full_name", "User")
    return render_template("dashboard.html", full_name=full_name)


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT id, full_name, email, password FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash (user[3], password):
            session["full_name"] = user[1]
            session["email"] = user[2]
            print("Login successful")
            return redirect(url_for("dashboard"))

        print("Login Failed")
        return render_template(
            "login.html",
            error = "Invalid email or password"
        )
    return render_template("login.html")

    
@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password)
        if full_name and email and password:
            
            cur = mysql.connection.cursor()
            cur.execute(
                """
                INSERT INTO users (full_name, email, password)
                VALUES (%s, %s, %s)
                """,
                (full_name, email, hashed_password),
            )
            mysql.connection.commit()
            cur.close()

        session["full_name"] = full_name or "User"
        return redirect(url_for("dashboard"))

    return render_template("sign_up.html")


#password route

@app.route("/analyze-password", methods=["POST"])
def analyze_password_route():

    data = request.get_json()

    password = data.get("password")

    result = analyze_password(password)

    return jsonify(result)

# password analyzer

import re

def analyze_password(password):

    score = 100
    issues = []

    # Length
    if len(password) < 12:
        score -= 20
        issues.append("Password should be at least 12 characters.")

    if len(password) < 16:
        score -= 10
        issues.append("Consider using 16+ characters for stronger security.")

    # Uppercase
    if not re.search(r"[A-Z]", password):
        score -= 15
        issues.append("Missing uppercase letters.")

    # Lowercase
    if not re.search(r"[a-z]", password):
        score -= 15
        issues.append("Missing lowercase letters.")

    # Numbers
    if not re.search(r"\d", password):
        score -= 15
        issues.append("Missing numbers.")

    # Special characters
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password):
        score -= 15
        issues.append("Missing special characters.")

    # Common passwords
    common_passwords = [
        "password",
        "password123",
        "123456",
        "qwerty",
        "admin",
        "welcome",
        "letmein"
    ]

    if password.lower() in common_passwords:
        score -= 50
        issues.append("Password is commonly used and easily guessed.")

    # Repeated characters
    if re.search(r"(.)\1\1", password):
        score -= 15
        issues.append("Contains repeated characters.")

    # Sequential patterns
    sequential = [
        "1234",
        "abcd",
        "qwer",
        "password"
    ]

    for patt in sequential:
        if patt in password.lower():
            score -= 15
            issues.append(f"Contains predictable sequence: {patt}")

    # Clamp score
    score = max(0, min(score, 100))

    # Security level
    if score >= 85:
        level = "Very Strong"
    elif score >= 70:
        level = "Strong"
    elif score >= 50:
        level = "Moderate"
    elif score >= 30:
        level = "Weak"
    else:
        level = "Very Weak"

    return {
        "score": score,
        "level": level,
        "issues": issues
    }


#URL route

@app.route("/analyze-url", methods=["POST"])
def analyze_url_route():

    data = request.get_json()

    url = data.get("url")

    result = analyze_url(url)

    return jsonify(result)

# URL Analyzer

def analyze_url(url):

    score = 100
    issues = []

    if not url.startswith("https://"):
        score -= 20
        issues.append(
            "Website is not using HTTPS"
        )

    if "@" in url:
        score -= 20
        issues.append(
            "Contains '@' symbol"
        )

    if len(url) > 75:
        score -= 10
        issues.append(
            "Unusually long URL"
        )

    score = max(0, score)

    return {
        "score": score,
        "issues": issues
    }


#Email Route

@app.route("/analyze-email", methods=["POST"])
def analyze_email_route():

    data = request.get_json()

    email = data.get("email")

    result = analyze_email(email)

    return jsonify(result)

#Email Analyzer

def analyze_email(email):

    score = 100
    issues = []

    urgency_words = [
        "urgent",
        "immediately",
        "act now",
        "limited time"
    ]

    for word in urgency_words:
        if word in email.lower():
            score -= 10
            issues.append(
                f'Urgency language detected: "{word}"'
            )

    credential_words = [
        "verify account",
        "confirm account",
        "reset password",
        "login now",
        "update payment"
    ]

    for word in credential_words:
        if word in email.lower():
            score -= 15
            issues.append(
                f'Credential request detected: "{word}"'
            )

    if "http://" in email:
        score -= 15
        issues.append(
            "Contains insecure HTTP link"
        )

    score = max(0, score)

    return {
        "score": score,
        "issues": issues
    }

@app.route("/assessment", methods=["GET", "POST"])
def assessment():

    password_result = None
    email_result = None
    url_result = None

    if request.method == "POST":

        assessment_type = request.form.get("type")

        if assessment_type == "password":

            password = request.form.get("password")

            password_result = analyze_password(password)

            print(password_result)
           

        elif assessment_type == "email":

            email_text = request.form.get("email_text")

            score = analyze_email(email_text)

            email_result = (
                "Likely Phishing"
                if score >= 2
                else "Looks Safe"
            )

        elif assessment_type == "url":

            url = request.form.get("url")

            url_result = analyze_url(url)

    return render_template(
        "assessment.html",
        password_result=password_result,
        email_result=email_result,
        url_result=url_result
    )
@app.route("/api/dashboard")
def dashboard_api():

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM password_checks")
    password_checks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM email_checks")
    emails_checks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM url_checks")
    urls_checks = cursor.fetchone()[0]

    return jsonify({
        "password_checked": password_checks,
        "emails_scanned": emails_checks,
        "urls_checked": urls_checks
   })


if __name__ == "__main__":
    app.run(debug=True)

   