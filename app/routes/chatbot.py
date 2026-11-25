from app.models.rag_model import DocumentChunk, Document, Conversation, Message
from extension import db
from app.services.rag_service import ask_rag
from flask import request, jsonify
from .main import main




@main.route("/api/chat", methods=["POST"])
def chat_api():

    data = request.get_json(silent=True) or {}

    question = data.get("message", "").strip()

    conversation_id = data.get("conversation_id")

    if not question:
        return jsonify({
            "error": "Message cannot be empty."
        }), 400

    if len(question) > 4000:
        return jsonify({
            "error": "Message is too long."
        }), 400

    try:

        if conversation_id:

            conversation = db.session.get(
                Conversation,
                conversation_id
            )

            if conversation is None:
                return jsonify({
                    "error": "Conversation not found."
                }), 404

        else:

            conversation = Conversation(
                title=question[:100]
            )

            db.session.add(conversation)
            db.session.flush()

        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=question
        )

        db.session.add(user_message)

        # Run RAG
        result = ask_rag(question)

        # Save AI response
        ai_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=result["answer"]
        )

        db.session.add(ai_message)

        db.session.commit()

        return jsonify({
            "answer": result["answer"],
            "conversation_id": conversation.id,
            "sources": result["sources"]
        })

    except Exception:
        db.session.rollback()

        return jsonify({
            "error": "Something went wrong. Please try again."
        }), 500
        
