from flask import Blueprint, jsonify
import random

name_generator_bp = Blueprint('name_generator', __name__)

@name_generator_bp.route("/generate-name", methods=["GET"])
def generate_name():
    adjectives = [
        "quick", "bright", "silent", "brave", "calm", "lucky", "sunny", "clever", "happy", "shiny"
    ]
    nouns = [
        "tiger", "hill", "cloud", "river", "falcon", "stone", "tree", "flame", "wave", "trail"
    ]

    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    number = str(random.randint(0, 9999)).zfill(4)

    name = f"{adjective}-{noun}-{number}"
    return jsonify({"name": name})
