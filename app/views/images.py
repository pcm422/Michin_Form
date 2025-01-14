from flask import Flask ,render_template
from app.models import ImageStatus ,Image ,db


# 이미지 생성
def create_image(url : str, image_type : ImageStatus) :
    new_image = Image(url=url, type = image_type)
    db.session.add(new_image)
    db.session.commit()
    return new_image.to_dict()

# 이미지 조회
def get_all_images() :
    images = Image.query.all()
    return images

def get_main_image() :
    image = Image.query.filter_by(type=ImageStatus.main).first()
    return image