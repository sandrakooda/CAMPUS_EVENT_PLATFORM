#!/usr/-bin/env python3
"""
Campus Event Management Platform - Prototype Implementation
A Flask-based REST API with SQLite database for demonstration purposes.
"""

from flask import Flask, request, jsonify, g, send_from_directory
from flask_cors import CORS
import sqlite3
import uuid
from datetime import datetime

# --- Step 1: Configure the Flask App ---
# This tells Flask to look for web files in the 'frontend' folder.
# This is the standard and most reliable way to set this up.
app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)
app.config['DATABASE'] = 'campus_events.db'


# --- Step 2: Create a Route for the Main Page ---
# This tells Flask what to do when someone visits the main URL (e.g., http://127.0.0.1:5000/)
@app.route('/')
def serve_index():
    """Serves the index.html file from the 'frontend' folder."""
    return send_from_directory(app.static_folder, 'index.html')


# --- Database Helper Functions (No Changes) ---
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.executescript('''
        CREATE TABLE IF NOT EXISTS colleges (id TEXT PRIMARY KEY, name TEXT NOT NULL, location TEXT, contact_email TEXT);
        CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, college_id TEXT NOT NULL, title TEXT NOT NULL, description TEXT, event_type TEXT NOT NULL, start_datetime TEXT NOT NULL, end_datetime TEXT NOT NULL, location TEXT, capacity INTEGER, status TEXT DEFAULT 'draft', created_by TEXT, FOREIGN KEY (college_id) REFERENCES colleges(id));
        CREATE TABLE IF NOT EXISTS students (id TEXT PRIMARY KEY, college_id TEXT NOT NULL, email TEXT UNIQUE NOT NULL, name TEXT NOT NULL, phone TEXT, year_of_study INTEGER, department TEXT, is_active BOOLEAN DEFAULT TRUE, FOREIGN KEY (college_id) REFERENCES colleges(id));
        CREATE TABLE IF NOT EXISTS registrations (id TEXT PRIMARY KEY, event_id TEXT NOT NULL, student_id TEXT NOT NULL, registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, status TEXT DEFAULT 'registered', FOREIGN KEY (event_id) REFERENCES events(id), FOREIGN KEY (student_id) REFERENCES students(id), UNIQUE(event_id, student_id));
        CREATE TABLE IF NOT EXISTS attendance (id TEXT PRIMARY KEY, event_id TEXT NOT NULL, student_id TEXT NOT NULL, checkin_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, status TEXT DEFAULT 'present', FOREIGN KEY (event_id) REFERENCES events(id), FOREIGN KEY (student_id) REFERENCES students(id), UNIQUE(event_id, student_id));
        CREATE TABLE IF NOT EXISTS feedback (id TEXT PRIMARY KEY, event_id TEXT NOT NULL, student_id TEXT NOT NULL, rating INTEGER, comments TEXT, FOREIGN KEY (event_id) REFERENCES events(id), FOREIGN KEY (student_id) REFERENCES students(id), UNIQUE(event_id, student_id));
        ''')
        db.executescript('''
    INSERT OR IGNORE INTO colleges (id, name, location, contact_email) VALUES ('MIT', 'Massachusetts Institute of Technology', 'Cambridge, MA', 'admin@mit.edu');
    INSERT OR IGNORE INTO students (id, college_id, email, name, department) VALUES ('MIT-STU-001', 'MIT', 'john.doe@mit.edu', 'John Doe', 'Computer Science');
    INSERT OR IGNORE INTO events (id, college_id, title, description, event_type, start_datetime, end_datetime, location, capacity, status) VALUES ('MIT-2025-001', 'MIT', 'Intro to AI Workshop', 'A beginner-friendly workshop on Artificial Intelligence.', 'workshop', '2025-10-15T10:00:00', '2025-10-15T13:00:00', 'Room 404', 50, 'active');
''')
        db.commit()
        print("Database initialized successfully.")

# --- API Routes (No Changes) ---
@app.route('/api/v1/colleges/<college_id>/events', methods=['GET'])
def get_events(college_id: str):
    db = get_db()
    events = db.execute('''
        SELECT e.*, 
               (SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id) as registration_count,
               (SELECT ROUND(AVG(f.rating), 1) FROM feedback f WHERE f.event_id = e.id) as avg_rating
        FROM events e WHERE e.college_id = ? ORDER BY e.start_datetime DESC
    ''', (college_id,)).fetchall()
    return jsonify([dict(row) for row in events])
# Add this entire function to app.py

@app.route('/api/v1/colleges/<college_id>/events/<event_id>/register', methods=['POST'])
def register_for_event(college_id, event_id):
    """Handles student registration for a specific event."""
    db = get_db()
    data = request.get_json()

    if not data or 'student_id' not in data:
        return jsonify({"error": "Student ID is required."}), 400

    student_id = data['student_id']

    # 1. Check if the event exists and get its capacity
    event = db.execute('SELECT capacity FROM events WHERE id = ?', (event_id,)).fetchone()
    if not event:
        return jsonify({"error": "Event not found."}), 404

    # 2. Check if the event is full
    registration_count = db.execute(
        'SELECT COUNT(*) FROM registrations WHERE event_id = ?', (event_id,)
    ).fetchone()[0]

    if event['capacity'] is not None and registration_count >= event['capacity']:
        return jsonify({"error": "Event is at full capacity."}), 409 # 409 Conflict

    # 3. Check if the student is already registered
    existing_registration = db.execute(
        'SELECT id FROM registrations WHERE event_id = ? AND student_id = ?',
        (event_id, student_id)
    ).fetchone()

    if existing_registration:
        return jsonify({"error": "Student is already registered for this event."}), 409

    # 4. If all checks pass, register the student
    try:
        new_reg_id = str(uuid.uuid4())
        db.execute(
            'INSERT INTO registrations (id, event_id, student_id) VALUES (?, ?, ?)',
            (new_reg_id, event_id, student_id)
        )
        db.commit()
        # After a successful registration, you might want to refetch the event data
        # to show the updated registration count on the front end.
        # For now, we'll just send a success message.
        return jsonify({
            "message": "Successfully registered for the event!",
            "registration_id": new_reg_id
        }), 201 # 201 Created
    except sqlite3.IntegrityError as e:
        # This is a fallback for race conditions or other DB constraints
        db.rollback()
        return jsonify({"error": "Database integrity error.", "details": str(e)}), 400

# ... other api routes would go here ...

# --- Main Execution ---
if __name__ == '__main__':
    init_db()
    # Host '0.0.0.0' makes it accessible on your network
    app.run(host='0.0.0.0', port=5000, debug=True)