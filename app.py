from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
import serial
import threading
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'yanyan'
db = SQLAlchemy(app)

socketio = SocketIO(app)
ser = serial.Serial('COM3', 9600, timeout=0.5)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Book {self.title}>"
    
def read_serial():
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            socketio.emit('serial_data', {'data': data})

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        book_title = request.form['title']
        book_author = request.form['author']
        book_year = request.form['year']

        if not all([book_year, book_title, book_year]):
            flash("All fields are required")
        else:
            new_book = Book(
                title=book_title,
                author=book_author,
                year=book_year  
            )

            try:
                db.session.add(new_book)
                db.session.commit()
                flash("Book added successfully")
            except Exception as e:
                db.session.rollback()
                flash(f"Error {str(e)}")

            return redirect("/")
        
    books = Book.query.order_by(Book.date_posted.desc()).all()
    return render_template("index.html", books=books)

@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    book = Book.query.get_or_404(id)

    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.year = int(request.form['year'])

        try:
            db.session.commit()
            flash("Book updated successfully.")
            return redirect("/")
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating book: {str(e)}")
            return redirect(url_for('edit', id=id))
        
    return render_template("edit.html", book=book)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    book = Book.query.get_or_404(id)

    try:
        db.session.delete(book)
        db.session.commit()
        flash("Book deleted successfully.")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting book: {str(e)}")

    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    thread = threading.Thread(target=read_serial)
    thread.daemon = True
    thread.start()
    socketio.run(app, host='0.0.0.0', port=4435, allow_unsafe_werkzeug=True)

    app.run(debug=True)