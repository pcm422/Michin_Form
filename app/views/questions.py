from app import db
from app.models import Question

# 질문 생성 함수
def create_question(title, image_id, sqe, is_active=True):
    new_question = Question(title=title, image_id=image_id, sqe=sqe, is_active=is_active)
    db.session.add(new_question)
    db.session.commit()
    return new_question

# 질문 조회 함수 (ID로 조회)
def get_question_by_id(question_id):
    question = Question.query.get(question_id)
    return question

# 모든 질문 조회 함수
def get_all_questions():
    questions = Question.query.all()
    return questions

def get_questions_count():
    count = Question.query.count()
    return count