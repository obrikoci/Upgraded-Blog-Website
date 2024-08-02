from flask import Flask, render_template, request
import requests
import smtplib

MY_EMAIL = "email"
PASSWORD = "password"

app = Flask(__name__)

all_posts = requests.get("https://api.npoint.io/8173277ab6648cb8c772").json()


@app.route('/')
def home_page():
    return render_template("index.html", posts=all_posts)


@app.route('/about')
def about_page():
    return render_template("about.html")

@app.route('/contact', methods=["GET", "POST"])
def contact_page():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone_nr = request.form["phone"]
        message = request.form["message"]
        send_email(name, email, phone_nr, message)
        return render_template("contact.html", sent=True)
    return render_template("contact.html", sent=False)


def send_email(name, email, phone, message):
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject: New Message from Blog\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
        )


@app.route('/post/<int:id>')
def read_post(id):
    for n_post in all_posts:
        if n_post['id'] == id:
            return render_template("post.html", post=n_post )


if __name__ == "__main__":
    app.run(debug=True)
