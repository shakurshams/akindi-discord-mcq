import os

from discord_interactions import (
    InteractionResponseType,
    InteractionType,
    InteractionResponseFlags,
    verify_key_decorator,
)
from flask import Flask, jsonify, request, Response

from app.config import (
    CLIENT_ID,
    CLIENT_SECRET,
    CLIENT_PUBLIC_KEY,
    DISCORD_API_VERSION,
    REDIRECT_URI,
)
from app.utils.misc_utils import (
    build_question_to_post_in_channel,
    get_questions_by_id,
)
from app.utils.api_utils import (
    get_api_access_token_from_authorization_code,
    post_question_to_channel_using_incoming_webhook,
)


app = Flask(__name__)

# unfortunate alternative to session which we are not using
global_cache = {}


@app.route("/")
def index():
    return "Hi"


@app.route("/oauth-redirect")
def oauth_redirect():
    code = request.args.get("code", None)

    if code:
        response = Response("Authorization code received successfully")

        @response.call_on_close
        def on_close():
            access_token, webhook = get_api_access_token_from_authorization_code(
                code=code
            )
            global_cache["access_token"] = access_token
            global_cache["webhook"] = webhook
            print(
                f"accesst_token = {global_cache['access_token']}, webhook = {global_cache['webhook']}"
            )

        return response

    else:
        return "Code was not sent", 400


@app.route("/send_question/<question_id>")
def send_question(question_id):
    if get_questions_by_id(id=question_id):

        quesion = build_question_to_post_in_channel(question_id)

        if post_question_to_channel_using_incoming_webhook(
            question=quesion, webhook_url=global_cache["webhook"]
        ):
            return "Successfully posted question to channel using incoming webhook"

        return "Could not post question to channel using incoming webhook", 400

    return "Wrong question_id", 404


@app.route("/receive_response", methods=["POST"])
@verify_key_decorator(CLIENT_PUBLIC_KEY)
def receive_response():
    interaction_type = request.json.get("type")
    interaction_data = request.json.get("data", {})
    interaction_member = request.json.get("member", {})

    if interaction_type == InteractionType.MESSAGE_COMPONENT:
        user_answer = interaction_data.get("custom_id", "").split("/")[-1]

        question_id = interaction_data.get("custom_id", "").split("/")[0]
        correct_answer = get_questions_by_id(id=question_id).get("answer")

        user_name = interaction_member.get("user", {}).get("username", "")
        user_id = interaction_member.get("user", {}).get("id", "")

        print(
            f"question_id = {question_id}, user_answer = {user_answer}, user_info = {user_name}/{user_id}"
        )

        return jsonify(
            {
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {
                    "content": f"Hi {user_name}/{user_id}, your answer is {user_answer}, correct answer is {correct_answer}",
                    "flags": InteractionResponseFlags.EPHEMERAL,
                },
            }
        )


if __name__ == "__main__":
    print(
        f"ENV variables are: CLIENT_ID = {CLIENT_ID}, CLIENT_SECRET = {CLIENT_SECRET}, CLIENT_PUBLIC_KEY = {CLIENT_PUBLIC_KEY}, DISCORD_API_VERSION = {DISCORD_API_VERSION}, REDIRECT_URI = {REDIRECT_URI}"
    )
    app.run(debug=True, host="127.0.0.1", port=os.getenv("PORT", default=5000))
