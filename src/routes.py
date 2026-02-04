from flask import Blueprint, jsonify, request
from models import db, User, Post, Comment, Media

api = Blueprint("api", __name__)

# 1 GET all users


@api.route('/users', methods=['GET'])
def get_users():

    users = User.query.all()
    response = [user.serialize() for user in users]
    return jsonify(response), 200


# POST agregar un nuevo registro o usuario a la lista

@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data.get('email') or not data.get('password') or not data.get('name'):

        return jsonify({"error": "name, email and password is required"}), 400
    # Ahora insertamos la funcion para un nuevo usuario
    new_user = User(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        is_active=True

    )

    db.session.add(new_user)
    # Ahora hacemos COMMIT y lo guardamos en la base de datos
    db.session.commit()
    # 201 significa que la solicitud al servidor fue exitosa y,
    return jsonify(new_user.serialize()), 201
    # como resultado, se ha creado un nuevo recurso

# DELETE USERS POR ID

@api.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

 # aqui se aplica el comando de borrado de alchemy
    db.session.delete(user)

    # hacemos el commit
    db.session.commit()
    # se borró el usuario con id indicado en la URL con éxito.
    return jsonify({"message": f"User {user.id} deleted"}), 200
