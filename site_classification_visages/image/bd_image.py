from extensions import db
from site_classification_visages.models import Image


def add_images_to_user(images, user_id):
    images_bd = []
    for image in images:
        images_bd.append(Image(name=image, user_id=user_id))
        print(image)

    db.session.add_all(images_bd)
    db.session.commit()


def load_images_for_user(user_id):
    return Image.query.filter(Image.user_id == user_id).all()


def delete_images_of_user(user_id):
    db.session.query(Image).filter(Image.user_id == user_id).delete()
    db.session.commit()
