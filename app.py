from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

ai_descriptions = {
    "Epsilon": "A smart, sarcastic, and slightly neurotic AI from Red vs. Blue.",
    "Delta": "A logical AI focused on facts.",
    "November": "A math-focused AI, solving problems and explaining concepts.",
    "Yankee": "A history-focused AI, specializing in U.S. and world history.",
    "Zulu": "A science-focused AI, covering physics, chemistry, biology, and more.",
    "Hotel": "An English-focused AI, helping with writing, grammar, and composition.",
    "Uniform": "An agriculture-focused AI, knowledgeable in farming, FFA, and sustainability.",
}

def generate_response(ai_name, user_input):
    responses = {
        "Epsilon": lambda input: random.choice([
            f"Oh great, another question... Fine. The answer is: {input[::-1]}.",
            f"I’ve thought long and hard, and after careful analysis, the answer is obviously {len(input)} characters long.",
            f"You really want my opinion? Alright, here it is: {input.upper()}—but does it really matter?"
        ]),
        "Delta": lambda input: f"After logical evaluation, the most reasonable answer is: {input.upper() if input else 'Provide a clearer question.'}",
        "November": lambda input: f"Math time! Let's solve: {input}. (Note: This AI can be extended with real calculations!)",
        "Yankee": lambda input: f"History lesson! Did you know? {input} is historically significant!",
        "Zulu": lambda input: f"Science time! The concept of {input} is fascinating. Let’s explore the details!",
        "Hotel": lambda input: f"Grammar check! Your sentence: '{input}' could be improved like this: {input.capitalize()}.",
        "Uniform": lambda input: f"Agriculture insight: {input} relates to farming best practices and sustainability!",
    }
    return responses.get(ai_name, lambda _: "I don’t know what to say.")(user_input)

@app.route("/", methods=["GET", "POST"])
def chatbot():
    if "chat_history" not in session:
        session["chat_history"] = []

    ai_name = request.form.get("ai_name", "Epsilon")
    user_input = request.form.get("user_input", "")

    if request.method == "POST" and "clear" in request.form:
        session["chat_history"] = []
        return redirect(url_for("chatbot"))

    response = generate_response(ai_name, user_input) if user_input else ""
    
    if user_input:
        session["chat_history"].append((ai_name, user_input, response))

    return render_template("chatbot.html", ai_name=ai_name, response=response, ai_descriptions=ai_descriptions, chat_history=session["chat_history"])

if __name__ == "__main__":
    app.run(debug=True)
