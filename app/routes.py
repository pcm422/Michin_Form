from flask import Blueprint, request, jsonify
from app import db
from app.views.users import create_user, get_all_users, get_user_by_id, delete_user
from app.views.questions import create_question, get_all_questions, get_question_by_id, update_question, delete_question
from app.views.choices import create_choice, get_all_choices
from app.views.answers import create_answer

# 유저 관련 블루프린트
user_bp = Blueprint('user',__name__)

# 유저 생성 API (회원가입)
@user_bp.route('/signup', methods = ['POST'])
def signup():
    data = request.json # 요청 데이터 받아오기 
    
    # 데이터값 가져오기
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    email = data.get('email')
    
    # 다 있는지 확인
    if not all([name, gender, age, email]) :
        return jsonify({'error' : '빈칸을 모두 채워주세요'}), 400
    
    # 유저생성함수
    new_user = create_user(name=name, age=age, gender=gender, email=email)
    
    # 유저정보 반환
    return jsonify({
        'message' : '회원 가입 성공 !',
        'user': new_user.to_dict() # 
    }) , 201

""" 유저 조회는 관리자 기능
# 특정 유저 조회 API   
@user_bp.route('/users/<int:user_id>', methods = ["GET"])
def get_user_bp(user_id):
    user = User.query.get(user_id) # user_id로 조회
    
    # 유저 없을시
    if user is None :
        return jsonify ({'error': '유저를 찾을 수 없습니다.'}), 404
    
    # 유저 있으면 정보반환
    return jsonify ({
        'user': user.to_dict()
    })
    
# 모든 유저 조회 API
@user_bp.route('/users',methods = ["GET"])
def get_all_users_bp():
    users = get_all_users()
    return jsonify ([user.to_dict() for user in users])
"""

# 질문 관련 블루프린트
questions_bp = Blueprint('questions', __name__)

# 질문 조회 API
@questions_bp.route('/questions', methods=['GET'])
def get_all_questions():
    questions = get_all_questions()
    return jsonify([q.to_dict() for q in questions]), 200


# 선택지 관련 블루프린트
choices_bp = Blueprint('choices', __name__)

# 선택지 조회 API
@choices_bp.route('/choices', methods=['GET'])
def get_all_choices():
    choices = get_all_choices()
    return jsonify([c.to_dict() for c in choices]), 200

# 선택지 생성 API
@choices_bp.route('/choices', methods=['POST'])
def create_choice():
    data = request.get_json()
    new_choice = create_choice(data['content'], data['question_id'], data['sqe'], data['is_active'])
    return jsonify(new_choice.to_dict()), 201


# 답변 관련 블루프린트
answers_bp = Blueprint('answers', __name__)

# 답변 생성 API
@answers_bp.route('/answers', methods=['POST'])
def create_answer():
    data = request.get_json()
    new_answer = create_answer(data['user_id'], data['choice_id'])
    return jsonify(new_answer.to_dict()), 201

""" 관리자 기능은 일단 모양만 갖춰놓음
# 관리자 관련 블루프린트
admin_bp = Blueprint('admin', __name__)

# 관리자 - 유저 조회 API
@admin_bp.route('/users', methods=['GET'])
def get_all_users():
    users = get_all_users()
    return jsonify([user.to_dict() for user in users]), 200

# 관리자 - 유저 삭제 API
@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    user = get_user_by_id(user_id)
    if user:
        delete_user(user_id)
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"message": "User not found"}), 404

# 관리자 - 질문 생성 API
@admin_bp.route('/questions', methods=['POST'])
def create_question_route():
    data = request.get_json()
    new_question = create_question(data['title'], data['image_id'], data['sqe'], data['is_active'])
    return jsonify(new_question.to_dict()), 201

# 관리자 - 질문 조회 API
@admin_bp.route('/questions/<int:question_id>', methods=['GET'])
def get_question_by_id_route(question_id):
    question = get_question_by_id(question_id)
    if question:
        return jsonify(question.to_dict()), 200
    return jsonify({"message": "Question not found"}), 404

# 관리자 - 질문 수정 API
@admin_bp.route('/questions/<int:question_id>', methods=['PUT'])
def update_question_route(question_id):
    data = request.get_json()
    question = get_question_by_id(question_id)
    if question:
        updated_question = update_question(question_id, data['title'], data['sqe'], data['is_active'])
        return jsonify(updated_question.to_dict()), 200
    return jsonify({"message": "Question not found"}), 404

# 관리자 - 질문 삭제 API
@admin_bp.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question_route(question_id):
    question = get_question_by_id(question_id)
    if question:
        delete_question(question_id)
        return jsonify({"message": "Question deleted successfully"}), 200
    return jsonify({"message": "Question not found"}), 404
"""