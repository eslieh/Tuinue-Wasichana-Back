from flask import Blueprint, request, jsonify
from models import db, Story, Charity
from datetime import datetime

story_bp = Blueprint('story', __name__, url_prefix='/stories')


# GET: Get all stories for a specific charity
@story_bp.route('/charity/<int:charity_id>', methods=['GET'])
def get_stories_for_charity(charity_id):
    charity = Charity.query.get(charity_id)
    if not charity:
        return jsonify({"error": "Charity not found."}), 404

    stories = Story.query.filter_by(charity_id=charity_id).all()
    return jsonify([{
        "id": s.id,
        "title": s.title,
        "content": s.content,
        "image_url": s.image_url,
        "created_at": s.created_at.strftime('%Y-%m-%d')
    } for s in stories]), 200


# POST: Create a new story (charity only)
@story_bp.route('/', methods=['POST'])
def post_story():
    data = request.get_json()

    required_fields = ['charity_id', 'title', 'content']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields."}), 400

    charity = Charity.query.get(data['charity_id'])
    if not charity:
        return jsonify({"error": "Charity not found."}), 404

    story = Story(
        charity_id=charity.id,
        title=data['title'],
        content=data['content'],
        image_url=data.get('image_url')  # optional
    )
    db.session.add(story)
    db.session.commit()

    return jsonify({
        "message": "Story created successfully.",
        "story": {
            "id": story.id,
            "title": story.title,
            "content": story.content,
            "image_url": story.image_url,
            "created_at": story.created_at.strftime('%Y-%m-%d')
        }
    }), 201
