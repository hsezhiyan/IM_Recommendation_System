from flask import Flask, render_template, request, url_for, redirect
from html_string import top_string, bottom_string
from userTagMatching import getRecommendations

app = Flask(__name__)

app.secret_key = b'\x9c!\x87\x12\x7f\xfc\xd9%%\xcc.0\xb8\x12\x1c\xbb'

@app.route("/", methods=["GET"])
def login_page():
	return render_template("search.html")

@app.route("/skills", methods=["GET"])
def skills():
	all_skills = request.args.getlist("skills")
	# Sairam's script goes here
	# queried_users = func(all_skills)
	queried_users = getRecommendations(all_skills)

	middle_string = ""
	for user in queried_users:
		middle_string += "<li method=\"post\">{}</li>".format(user)

	return top_string + middle_string + bottom_string

if __name__ == "__main__":
	app.run()
