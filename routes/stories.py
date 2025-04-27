from flask import Blueprint, request, jsonify
from models.story import Story
from models.charity import Charity
from config import db
from sqlalchemy.exc import SQLAlchemyError
from auth import charity_required

stories_bp = Blueprint('stories_bp', __name__, url_prefix='/stories')

@stories_bp.route('', methods=['POST'])
@charity_required
def create_story():
    data = request.get_json()
    try:
        new_story = Story(
            charity_id=data.get("charity_id"),
            title=data.get("title"),
            content=data.get("content"),
            image_url=data.get("image_url")
        )
        db.session.add(new_story)
        db.session.commit()
        return jsonify(new_story.to_dict()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@stories_bp.route('', methods=['GET'])
def get_stories():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    stories = Story.query.order_by(Story.created_at.desc()).paginate(page=page, per_page=per_page)
    return jsonify({
        "stories": [story.to_dict() for story in stories.items],
        "total": stories.total,
        "pages": stories.pages,
        "current_page": page
    }), 200

@stories_bp.route('/charities/<int:charity_id>', methods=['GET'])
def get_charity_stories(charity_id):
    charity = Charity.query.get(charity_id)
    if not charity:
        return jsonify({"error": "Charity not found"}), 404
    
    stories = Story.query.filter_by(charity_id=charity_id).all()
    return jsonify([story.to_dict() for story in stories]), 200