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



# password analysis
def check_password(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
   
    if score <=2 :
        strength = "Weak"
    if score == 3:
        strength = "Medium"
    else:
        strength = "strong"

    return score, strength

# Email analysis
def check_email(email_text):
    suspicious_words = [
        "urgent",
        "click here",
        "verify account",
        "winner",
        "free money",
    ]
    score = 0

    for word in suspicious_words:
        if word.lower() in email_text.lower():
            score += 1
    return score


# URL safety check
def check_url(url):

    if not url.startswith("https://"):
        return "Suspicious"

    if "@" in url:
        return "Suspicious"

    return "Safe"

@app.route("/assessment", methods=["GET", "POST"])
def assessment():

    password_result = None
    email_result = None
    url_result = None

    if request.method == "POST":

        assessment_type = request.form.get("type")

        if assessment_type == "password":

            password = request.form.get("password")

            score, strength = check_password(password)

            password_result = {
                "score": score,
                "strength": strength
            }

        elif assessment_type == "email":

            email_text = request.form.get("email_text")

            score = check_email(email_text)

            email_result = (
                "Likely Phishing"
                if score >= 2
                else "Looks Safe"
            )

        elif assessment_type == "url":

            url = request.form.get("url")

            url_result = check_url(url)

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

   