import panel as pn
from openai import OpenAI

# ------------------ PANEL SETUP ------------------
pn.extension()

# ------------------ OPENAI CLIENT ----------------
client = OpenAI(api_key="API_KEY")
  # uses OPENAI_API_KEY from environment

# ------------------ CHAT CONTEXT -----------------
context = [
    {
        "role": "system",
        "content": "You are OrderBot, a friendly assistant that helps users place food orders."
    }
]

# ------------------ OPENAI FUNCTION ---------------
def get_completion_from_messages(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# ------------------ UI COMPONENTS -----------------
chat_box = pn.Column(
    pn.pane.Markdown(
        "👋 **Hello! I am OrderBot.**\n\nWhat would you like to order?",
        width=400,
        styles={
            "background": "#F6F6F6",
            "padding": "10px",
            "border-radius": "8px"
        }
    )
)

user_input = pn.widgets.TextInput(
    placeholder="Type your order here...",
    width=400
)

send_button = pn.widgets.Button(
    name="Send",
    button_type="primary",
    width=100
)


# ------------------ CALLBACK FUNCTION -------------
def collect_messages(event):
    user_message = user_input.value.strip()
    if not user_message:
        return

    # Show user message
    chat_box.append(
        pn.pane.Markdown(
            f"🧑 **You:** {user_message}",
            width=400,
            styles={
                "background": "#E8F0FE",
                "padding": "8px",
                "border-radius": "8px"
            }
        )
    )

    context.append({"role": "user", "content": user_message})

    # Get bot reply
    bot_reply = get_completion_from_messages(context)
    context.append({"role": "assistant", "content": bot_reply})

    # Show bot reply
    chat_box.append(
        pn.pane.Markdown(
            f"🤖 **OrderBot:** {bot_reply}",
            width=400,
            styles={
                "background": "#F1F8E9",
                "padding": "8px",
                "border-radius": "8px"
            }
        )
    )

    user_input.value = ""


# ------------------ BUTTON BIND -------------------
send_button.on_click(collect_messages)

# ------------------ APP LAYOUT --------------------
app = pn.Column(
    "## 🛒 Order Bot",
    chat_box,
    user_input,
    send_button,
    sizing_mode="stretch_width"
)

# ------------------ SERVE APP ---------------------
app.servable()

