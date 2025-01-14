from app import db
from app.models import User

# 유저 생성 함수
def create_user(name, age, gender, email):
    # 이메일 중복 체크
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return None  # 중복된 이메일이면 None 반환
    
    new_user = User(name=name, age=age, gender=gender, email=email)
    db.session.add(new_user)
    db.session.commit()
    return new_user

# 유저 조회 함수 (ID로 조회)
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    return user

# 모든 유저 조회 함수
def get_all_users():
    users = User.query.all()
    return users