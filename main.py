from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)


def __repr__(self):
    return f'<Book {self.title}>'


with app.app_context():
    db.create_all()
#
#
# with app.app_context():
#     new_book = Book(
#         title="Harry Potter and the Chamber of Secrets",
#         author="J. K. Rowling",
#         rating=9.6,
#     )
#     db.session.add(new_book)
#     db.session.commit()

# with app.app_context():
#     result = db.session.execute(db.select(Book).order_by(Book.title))
#     books = result.scalars().all()


# for book in books:
#     print(f"{book.id}: {book.title} by {book.author} - Rating: {book.rating}")


# with app.app_context():
#     result = db.session.execute(db.select(Book).where(Book.id == 3)).scalar()
#     db.session.delete(result)
#     db.session.commit()


@app.route('/')
def home():
    books = db.session.execute(db.select(Book).order_by(Book.title)).scalars().all()
    return render_template('index.html', books=books, books_added=bool(books))


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form['book_name'],
            author=request.form['book_author'],
            rating=request.form['rating']
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    book_to_update = db.get_or_404(Book, id)
    if request.method == "POST":
        book_to_update.rating = request.form['new_rating']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", books=book_to_update)


@app.route('/delete/<int:id>')
def delete(id):
    book_to_delete = db.get_or_404(Book, id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

