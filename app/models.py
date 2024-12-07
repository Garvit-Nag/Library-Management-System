from typing import List, Dict, Optional
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
import hashlib
import os

@dataclass
class Book:
    id: Optional[int] = None
    title: str = ''
    author: str = ''
    isbn: str = ''
    published_year: int = 0
    available: bool = True

@dataclass
class Member:
    id: Optional[int] = None
    name: str = ''
    email: str = ''
    borrowed_books: List[int] = field(default_factory=list)

@dataclass
class Token:
    user_id: int
    expires_at: datetime
    token: str = ''

class Database:
    def __init__(self, path: str):
        self.path = path
        self.books: List[Book] = []
        self.members: List[Member] = []
        self.tokens: List[Token] = []
        self.book_id_counter = 1
        self.member_id_counter = 1

    def generate_token(self, user_id: int) -> str:
        token = hashlib.sha256(os.urandom(60)).hexdigest()
        expires_at = datetime.now() + timedelta(hours=1)
        self.tokens.append(Token(user_id=user_id, token=token, expires_at=expires_at))
        return token

    def validate_token(self, token: str) -> Optional[int]:
        for t in self.tokens:
            if t.token == token and t.expires_at > datetime.now():
                return t.user_id
        return None

    def add_book(self, book: Book) -> Book:
        book.id = self.book_id_counter
        self.book_id_counter += 1
        self.books.append(book)
        return book

    def add_member(self, member: Member) -> Member:
        member.id = self.member_id_counter
        self.member_id_counter += 1
        self.members.append(member)
        return member

    def get_book(self, book_id: int) -> Optional[Book]:
        return next((book for book in self.books if book.id == book_id), None)

    def get_member(self, member_id: int) -> Optional[Member]:
        return next((member for member in self.members if member.id == member_id), None)

    def update_book(self, book_id: int, updated_book: Book) -> Optional[Book]:
        for i, book in enumerate(self.books):
            if book.id == book_id:
                updated_book.id = book_id
                self.books[i] = updated_book
                return updated_book
        return None

    def update_member(self, member_id: int, updated_member: Member) -> Optional[Member]:
        for i, member in enumerate(self.members):
            if member.id == member_id:
                updated_member.id = member_id
                self.members[i] = updated_member
                return updated_member
        return None

    def delete_book(self, book_id: int) -> bool:
        self.books = [book for book in self.books if book.id != book_id]
        return True

    def delete_member(self, member_id: int) -> bool:
        self.members = [member for member in self.members if member.id != member_id]
        return True

    def search_books(self, query: str) -> List[Book]:
        return [
            book for book in self.books 
            if query.lower() in book.title.lower() or query.lower() in book.author.lower()
        ]

    def list_books(self, page: int, page_size: int) -> List[Book]:
        start = (page - 1) * page_size
        end = start + page_size
        return self.books[start:end]