from flask import Flask, request, jsonify
from typing import Dict, Any
from .models import Database, Book, Member
from config import Config
from .utils import require_auth

class LibraryApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.db = Database(Config.DATABASE_PATH)
        self.app.db = self.db
        
    def create_routes(self):
        @self.app.route('/books', methods=['POST'])
        @require_auth
        def create_book():
            data: Dict[str, Any] = request.get_json()
            book = Book(**data)
            created_book = self.db.add_book(book)
            return jsonify(created_book.__dict__), 201

        @self.app.route('/books', methods=['GET'])
        @require_auth
        def get_books():
            page = int(request.args.get('page', 1))
            books = self.db.list_books(page, Config.PAGE_SIZE)
            return jsonify([book.__dict__ for book in books])

        @self.app.route('/books/search', methods=['GET'])
        @require_auth
        def search_books():
            query = request.args.get('q', '')
            books = self.db.search_books(query)
            return jsonify([book.__dict__ for book in books])

        @self.app.route('/books/<int:book_id>', methods=['GET'])
        @require_auth
        def get_book(book_id: int):
            book = self.db.get_book(book_id)
            return jsonify(book.__dict__) if book else ('', 404)

        @self.app.route('/books/<int:book_id>', methods=['PUT'])
        @require_auth
        def update_book(book_id: int):
            data: Dict[str, Any] = request.get_json()
            book = Book(**data)
            updated_book = self.db.update_book(book_id, book)
            return jsonify(updated_book.__dict__) if updated_book else ('', 404)

        @self.app.route('/books/<int:book_id>', methods=['DELETE'])
        @require_auth
        def delete_book(book_id: int):
            result = self.db.delete_book(book_id)
            return ('', 204) if result else ('', 404)

        # Similar authentication added to member routes...
        @self.app.route('/members', methods=['POST'])
        def create_member():
            data: Dict[str, Any] = request.get_json()
            member = Member(**data)
            created_member = self.db.add_member(member)
            return jsonify(created_member.__dict__), 201

        @self.app.route('/members/<int:member_id>', methods=['GET'])
        @require_auth
        def get_member(member_id: int):
            member = self.db.get_member(member_id)
            return jsonify(member.__dict__) if member else ('', 404)

        @self.app.route('/members/<int:member_id>', methods=['PUT'])
        @require_auth
        def update_member(member_id: int):
            data: Dict[str, Any] = request.get_json()
            member = Member(**data)
            updated_member = self.db.update_member(member_id, member)
            return jsonify(updated_member.__dict__) if updated_member else ('', 404)

        @self.app.route('/members/<int:member_id>', methods=['DELETE'])
        @require_auth
        def delete_member(member_id: int):
            result = self.db.delete_member(member_id)
            return ('', 204) if result else ('', 404)

        @self.app.route('/auth/token', methods=['POST'])
        def generate_token():
            member_id = request.get_json().get('member_id')
            member = self.db.get_member(member_id)
            if member:
                token = self.db.generate_token(member_id)
                return jsonify({"token": token})
            return jsonify({"error": "Member not found"}), 404

        return self.app

def create_app():
    library_app = LibraryApp()
    return library_app.create_routes()