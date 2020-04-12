from flask import Flask, render_template, request
import requests
import re


"""
imports a dictionary of data from dog_breeds.py and "prettifies",
or styles, the dog names when they appear in the HTML page
"""

from dog_breeds import prettify_dog_breed

app = Flask("app")


# function adds a dash in the URL between breed names with multiple words like miniature poodle
def check_breed(breed):
    return "/".join(breed.split("-"))


@app.route("/", methods=["GET", "POST"])
def dog_image_gallery():
    errors = []
    if request.method == "POST":
        breed = request.form.get("breed")
        number = request.form.get("number")
        if not breed:
            errors.append("Oops - please select a breed.")
        if not number:
            errors.append("Oops - please select a number")
        if breed and number:
            response = requests.get(
                "https://dog.ceo/api/breed/"
                + check_breed(breed)
                + "/images/random/"
                + number
            )
            data = response.json()
            print(data)
            dog_images = data["message"]
            return render_template(
                "dogs.html", images=dog_images, breed=prettify_dog_breed(breed)
            )

    # If you get here, you've made a GET request
    return render_template("dogs.html", errors=errors)


@app.route("/random", methods=["POST"])
def get_random():
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    data = response.json()
    dog_images = [data["message"]]
    # Extract the breed name from the dog_image
    breed = re.compile("breeds/(.*)$").search(dog_images[0]).group(1).split("/")[0]
    try:
        breed = prettify_dog_breed(breed)
    except KeyError:
        breed = "Random Doggo"

    random = True
    return render_template("dogs.html", images=dog_images, random=random, breed=breed)


app.debug = True
app.run(host="0.0.0.0", port=8080)
