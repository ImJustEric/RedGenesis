from flask import redirect, render_template, session, Flask, request, jsonify
from openai import OpenAI
import base64
import os

# For keeping website alive every 14 minutes 
import threading
import requests
import time

# Configure application 
app = Flask(__name__)

# Where the website will be held 
@app.route("/")
def index():
    return render_template("index.html")


# Where the AI prompt will be taken 
@app.route("/response", methods=['POST'])
def response():
    surgeries = request.form['surgeries']
    surgeries_list = [surgery.strip() for surgery in surgeries.split(',')]


    part_prompt = {
        "Vestibular Recalibration": "Highlighting the brain to show the use of vestibular calibration, where the brain is adapted and rehabilitated to low gravity to prevent from space sickness",
        "Ocular Augmentation": "Re-coloring of the eyes to show that the eyes have been updated to protect from UV rays and to work in low-light situations",
        "Myostatin Gene Suppression": "Strengthened muscle fibers in the body to show that the body has been augmented to prevent muscle atrophy in low gravity settings",
        "Embedded Micro-oxygenators": "A micro pump system embedded inside the lungs, to simulate allowing oxygen into the bloodstream during low-pressure exposures",
        "Boosted Cytochrome P450 Enzymes": "A magnification into the proteins of the body of the human showing that there are boosted enzymes that help detoxify sulfuric gases and chemicals",
        "Iron Nanoparticle Skin Implants": "Skin tissue naturally infused with iron-binding proteins and nanostructures to shield against radiation",
        "Ferritin Overexpression": "A magnification into the proteins of the the body containing ferritin, showing that it has been improved to store more iron"
    }

    # Structure the prompt 
    
    prompt_intro = (
        "Give me a picture of a human outline, similar to the human being cut in half from the front "
        "so that you basically have an outline of the body parts and the skeleton of the human, "
        "but the human has these upgrades as it now lives on Mars: "
    )
    prompt_input = "; ".join(part_prompt[surgery] for surgery in surgeries_list if surgery in part_prompt)
    prompt_end = f". Make sure to not include any labels and make it seem more scientific."

    final_prompt = prompt_intro + prompt_input + prompt_end

    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        result = client.images.generate(
            model="dall-e-3",
            prompt= final_prompt,
            n=1,
            size="1024x1024",
            response_format="b64_json"
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

    except Exception:
        with open('static/default_body.png', 'rb') as f:
            image_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    return jsonify({'image_bytes': image_base64})
    

# Function to keep website alive 
def self_ping():
    while True:
        try:
            print("Self-pinging to stay awake...")
            requests.get("https://redgenesis.onrender.com/")
        except Exception as e:
            print(f"Ping failed: {e}")
        time.sleep(780)  # Ping every 13 minutes

if __name__ == "__main__":
    # Start self-pinging in the background 
    threading.Thread(target=self_ping, daemon=True).start()
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
