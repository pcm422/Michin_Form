from flask import request, jsonify, session
from flask_smorest import Blueprint
from app import db
from app.views.users import create_user
from app.views.questions import get_question_by_id, get_questions_count, create_question
from app.views.choices import create_choice, get_choices_by_question_id
from app.views.answers import create_answer, get_user_by_id, get_choice_by_id
from app.views.images import get_main_image, create_image

# 유저 관련 블루프린트
user_bp = Blueprint('Users', 'users')

@user_bp.route("/")
def hello():
    return jsonify({"message": "Success Connect"})

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
    try:
        if not new_user:
            raise ValueError('이미 존재하는 계정 입니다.')
    except ValueError as ve:
        return jsonify({
        'error': '이미 존재하는 계정 입니다.'
    }), 301

    # 유저 정보 반환
    return jsonify({
        'message': f'{new_user.name}님 회원가입을 축하합니다',
        'user_id': new_user.id
    }), 201

# 질문 관련 블루프린트
questions_bp = Blueprint('Questions', 'questions')

# 특정 질문 조회 API
@questions_bp.route('/question/<int:question_id>', methods=['GET'])
def get_question(question_id):
    # 질문 가져오기
    question = get_question_by_id(question_id)
    if not question:
        return jsonify({'error': '해당 질문을 찾을 수 없습니다.'}), 404

    # 해당 질문의 선택지 가져오기 (효율적인 쿼리 사용)
    choices = get_choices_by_question_id(question_id)  # 선택지를 직접 필터링
    filtered_choices = [
        {
            'id': choice.id,
            'content': choice.content,
            'is_active': choice.is_active
        } for choice in choices
    ]

    # 순서를 맞추기 위해 딕셔너리 순서대로 배치
    response_data = {
        'question' : {
            'id': question.id,
            'title': question.title,
            'image': {'url': question.image.url if question.image else None},  # 이미지가 있을 때만 URL 반환
            'choices': filtered_choices
        }
    }

    return jsonify(response_data), 200

# 질문 갯수 구하는 API
@questions_bp.route('/questions/count', methods=['GET'])
def get_question_count():
    count = get_questions_count()
    return jsonify({'total': count}), 200

# 질문 생성 API
@questions_bp.route('/question', methods=['POST'])
def add_question():
    data = request.get_json()

    title = data.get('title')
    image_id = data.get('image_id')
    sqe = data.get('sqe')
    is_active = data.get('is_active', True)  # 기본값 True

    if not title or not image_id or not sqe:
        return jsonify({'error': 'title, image_id, sqe는 필수입니다.'}), 400

    try:
        new_question = create_question(title, image_id, sqe, is_active)
        return jsonify({
            'message': f'Title: {new_question.title} question Success Create'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 선택지 관련 블루프린트
choices_bp = Blueprint('choice', __name__)

# 선택지 생성 API
@choices_bp.route('/choice', methods=['POST'])
def add_choice():
    data = request.get_json()

    content = data.get('content')
    sqe = data.get('sqe')
    question_id = data.get('question_id')

    # 필수 값 체크
    if not content or not sqe or not question_id:
        return jsonify({'error': 'content, sqe, question_id는 필수입니다.'}), 400

    try:
        new_choice = create_choice(content, sqe, question_id)
        return jsonify({
            'message': f'Content: {new_choice.content} choice Success Create'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 질문 아이디로 선택지 조회 API
@choices_bp.route('/choice/<int:question_id>', methods=['GET'])
def get_choice_by_question_id(question_id):
    # 해당 question_id에 대한 선택지들을 가져오기
    choices = get_choices_by_question_id(question_id)
    
    # 선택지들을 리스트로 가공, 필요한 필드만 포함시킴
    filtered_choices = [
        {
            "id": choice.id,  # id
            "content": choice.content,  # content
            "is_active": choice.is_active  # is_active
        }
        for choice in choices
    ]
    
    # 선택지 리스트를 JSON 형식으로 반환
    return jsonify({"choices": filtered_choices}), 200

# 이미지 관련 블루프린트
image_bp = Blueprint('image', __name__)

# 이미지 생성 API
@image_bp.route('/image', methods=['POST'])
def create_image_route():
    data = request.json  # 사용자로부터 받은 데이터
    
    # 데이터 값 확인
    image_url = data.get('url')
    image_type = data.get('type')
    
    if not image_url or not image_type:
        return jsonify({'error': 'url 또는 type이 없습니다.'}), 400
    
    # 이미지 생성 함수 호출
    new_image = create_image(image_url, image_type)
    
    # 성공 메시지 반환
    return jsonify({'message': f'ID: {new_image.id} Image Success Create'}), 201

# 메인 이미지 조회 API  
@image_bp.route('/image/main', methods=['GET'])
def get_image():
    image = get_main_image()
    if not image:
        return jsonify({'error': 'Main image not found'}), 404
    
    return jsonify({'image': image.url}), 200

# 답변 관련 블루프린트
answers_bp = Blueprint('answers', __name__)

# 답변 생성 API
@answers_bp.route('/answers', methods=['POST'])
def create_answers():
    data = request.get_json()
    new_answer = create_answer(data['user_id'], data['choice_id'])
    return jsonify(new_answer.to_dict()), 201

# 답변 제출 API
@questions_bp.route('/submit', methods=['POST'])
def submit_answers():
    try:
        data = request.json  # 요청 데이터 받기
        if not data or not isinstance(data, list):
            return jsonify({'error': '유효하지 않은 데이터 형식입니다.'}), 400

        for item in data:
            # userId와 choiceId를 정수로 변환
            user_id = int(item.get('userId'))
            choice_id = int(item.get('choiceId'))

            if not user_id or not choice_id:
                return jsonify({'error': 'userId와 choiceId는 필수입니다.'}), 400

            # 유저와 선택지 조회
            user = get_user_by_id(user_id)
            choice = get_choice_by_id(choice_id)

            if not user:
                return jsonify({'error': f'User ID {user_id}를 찾을 수 없습니다.'}), 404
            if not choice:
                return jsonify({'error': f'Choice ID {choice_id}를 찾을 수 없습니다.'}), 404

            # 답변 저장
            create_answer(user_id, choice_id)

        return jsonify({'message': '답변 저장 성공'}), 201

    except Exception as e:
        print("Error occurred:", str(e))  # 에러 메시지 출력
        return jsonify({'error': '서버 내부 오류 발생'}), 500

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