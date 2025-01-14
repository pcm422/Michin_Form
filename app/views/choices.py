from app import db
from app.models import Choices

# 선택지 생성 함수
def create_choice(content, question_id, sqe, is_active=True):
    new_choice = Choices(content=content, question_id=question_id, sqe=sqe, is_active=is_active)
    db.session.add(new_choice)
    db.session.commit()
    return new_choice

# 선택지 조회 함수 (ID로 조회)
def get_choice_by_id(choice_id):
    choice = Choices.query.get(choice_id)
    return choice

# 모든 선택지 조회 함수
def get_all_choices():
    choices = Choices.query.all()
    return choices

def get_choices_by_question_id(question_id):
    # 주어진 question_id에 해당하는 선택지들을 가져오기
    return Choices.query.filter_by(question_id=question_id).all()