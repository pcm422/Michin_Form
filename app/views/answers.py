from app import db
from app.models import Answer

# 답변 생성 함수
def create_answer(user_id, choice_id):
    new_answer = Answer(user_id=user_id, choice_id=choice_id)
    db.session.add(new_answer)
    db.session.commit()
    return new_answer

# 답변 조회 함수 (ID로 조회)
def get_answer_by_id(answer_id):
    answer = Answer.query.get(answer_id)
    return answer

# 모든 답변 조회 함수
def get_all_answers():
    answers = Answer.query.all()
    return answers