from fileinput import filename

from flask import Flask, render_template, redirect, url_for, request  # pyright: ignore[reportMissingImports]
from flask_mysqldb import MySQL  # pyright: ignore[reportMissingImports]

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static",
)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "security_app"

mysql = MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":

        print(request.form)

        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")

        cur = mysql.connection.cursor()

        cur.execute(
            """
            INSERT INTO users (full_name, email, password)
            VALUES (%s, %s, %s)
            """,
            (full_name, email, password)
        )

        mysql.connection.commit()
        cur.close()

        return redirect(url_for("dashboard"))

    return render_template("sign_up.html")
@app.route("/assessment")
def assessment():
    return render_template("assessment.html")
#password analysis
def check_password(password):
    score = 0
    if len(password) >= 8:
        score +=1
    if any(c.isupper() for c in password):
        score +=1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit()for c in password):
        score +=1
    return score
#Email analysis
def check_email(email_text):
    suspicious_word = [
        "urgent",
        "click here",
        "verify account",
        "winner",
        "free money"
    ]
    score = 0
    for word in suspicious_word:
        if word.lower() in email_text.lower():
            score += 1
    return score

#URL safety check
def check_url(url):
    if not url.startswith("https://"):
        return "Suspicious"
    if "@" in url:
        return "Suspicious"
    return "Safe"
if __name__ == "__main__":
    app.run(debug=True)

