import json


def get_questions():
    with open("app/questions.json") as f:
        return json.load(f)


def get_questions_by_id(id):
    questions = get_questions()
    return questions.get(id, None)


def build_answer_choices_components_from_question(question_id):
    question = get_questions_by_id(id=question_id)
    return [
        {
            "type": 2,
            "label": option_text,
            "style": 1,
            "custom_id": f"{question_id}/{option_id}",
        }
        for option_id, option_text in question.get("options", {}).items()
    ]


def build_question_to_post_in_channel(question_id):
    components = build_answer_choices_components_from_question(question_id=question_id)
    content = get_questions_by_id(id=question_id).get("content", "")

    return {
        "content": content,
        "components": [
            {
                "type": 1,
                "components": components,
            }
        ],
    }
