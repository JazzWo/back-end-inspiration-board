from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card


cards_bp = Blueprint("cards_bp", __name__, url_prefix=("/cards"))

#Creating a card
@cards_bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()
    try:
        new_card = Card.from_dict(request_body)
        if len(new_card.message) > 40:
            return make_response({"Error": "Expected length exceeded"})
        db.session.add(new_card)
        db.session.commit()
        return make_response(request_body, 201)
    except KeyError:
        response = {
            "details" : "Invalid request body"
        }

        abort(make_response(response, 400))

   
@cards_bp.route('', methods=['GET'])
def view_all_cards():
    cards = Card.query.all()
    card_response = []
    for card in cards:
        card_response.append(card.to_dict())
    return jsonify(card_response)

#Deleting a card
@cards_bp.route("<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = Card.query.get(card_id)
    if not card:
        return jsonify({'message' : f'Card {card_id} was not found'}), 404
    db.session.delete(card)
    db.session.commit()
    return jsonify({
        'id': card.card_id,
        'details': f'Card {card.card_id} succesfully deleted'}), 200

#Adding a +1
@cards_bp.route("<card_id>", methods=["PATCH"])
def update_card(card_id):
    # request_body = request.get_json()
    card = Card.query.get(card_id)
    if card is None:
        return jsonify(None), 404

    card.likes_count += 1
    db.session.commit()

    return jsonify(card.to_dict()), 200



