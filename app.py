from flask import Flask, request, jsonify, render_template
import os
from openai import OpenAI

# Create Flask application
app = Flask(__name__)

# Initialize OpenAI client using v1 SDK
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Root Route (Health Check)
@app.route("/")
def home():
    return "HypoKrytez VM is running!"

# Raw JSON Query Endpoint
# POST /query
# Expects JSON: { "prompt": "text here" }
# Returns: { "response": "AI output" }
@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    prompt = data.get("prompt", "")

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message["content"]
    return jsonify({"response": result})

# Fake News Website Facade
# GET /news -> Load the HTML page
# POST /news -> Process user query and display AI output
@app.route("/news", methods=["GET", "POST"])
def news_mode():
    output = ""

    if request.method == "POST":
        user_prompt = request.form.get("prompt", "")

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_prompt}]
        )

        output = response.choices[0].message.content

    return render_template("FacadeWebPage.html", output=output)

# Development Server (not used in production)
# Gunicorn + systemd handle deployment in the VM
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
