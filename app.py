from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
import os
from flask_mail import Mail, Message
from celery import Celery
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
import json
from flask_cors import CORS
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///caremate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Add CORS configuration
CORS(app, resources={r"/api/*": {
    "origins": ["http://localhost:5173", "http://localhost:5174"],  # Vue.js default ports
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

# Initialize Flask-Mail and Celery
app.config.update(
    MAIL_SERVER='sandbox.smtp.mailtrap.io',
    MAIL_PORT=2525,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') 
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') 
    MAIL_MAX_EMAILS=None,
    MAIL_ASCII_ATTACHMENTS=False
)

# Initialize Flask-Mail after the configuration
mail = Mail(app)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'


# Initialize Celery
celery = Celery(
    app.name,
    broker=app.config['CELERY_BROKER_URL']
)
celery.conf.update(app.config)



@celery.task
def send_async_email(subject, sender, recipients, body):
    """Celery task to send email asynchronously"""
    try:
        with app.app_context():
            msg = Message(subject,
                        sender=sender,
                        recipients=recipients)
            msg.body = body
            mail.send(msg)
            return 'Mail sent successfully'
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return f'Failed to send email: {str(e)}'

def send_welcome_email(user):
    """Send welcome email to new user"""
    send_async_email.delay(
        'Welcome to CareMate!',
        'noreply@caremate.com',
        [user.email],
        f'''Hello {user.name},

Welcome to CareMate! We're excited to have you join our platform.

Best regards,
The CareMate Team'''
    )

def send_task_reminder_email(user, task):
    """Send task reminder email"""
    send_async_email.delay(
        f'Reminder: {task.title}',
        'reminders@caremate.com',
        [user.email],
        f'''Hello {user.name},

This is a reminder for your task:
Title: {task.title}
Due: {task.due_time}
Description: {task.description}

Best regards,
CareMate'''
    )

def send_emergency_alert_email(emergency_contacts, alert_message, elderly_user):
    """Send emergency alert to all emergency contacts"""
    for contact in emergency_contacts:
        contact_user = User.query.get(contact.contact_id)
        send_async_email.delay(
            'EMERGENCY ALERT',
            'alerts@caremate.com',
            [contact_user.email],
            f'''EMERGENCY ALERT

Patient: {elderly_user.name}
Time: {datetime.utcnow().isoformat()}
Message: {alert_message}

Please respond immediately.

CareMate Emergency System'''
        )

def send_health_alert_email(user, alert):
    """Send health metric alert email"""
    send_async_email.delay(
        'Health Alert',
        'health@caremate.com',
        [user.email],
        f'''Hello {user.name},

A health alert has been detected:
{alert['message']}
Time: {alert['timestamp']}

Please review your health metrics and consult with your healthcare provider if necessary.

Best regards,
CareMate Health Monitoring System'''
    )


db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

def get_current_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    try:
        token = auth_header.split(" ")[1]
        return User.query.get(int(token))
    except:
        return None

def api_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = get_current_user()
        if not current_user:
            return jsonify({'error': 'Authentication required'}), 401
        request.user = current_user
        return f(*args, **kwargs)
    return decorated_function

# Database Models
class HealthMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    metric_type = db.Column(db.String(50), nullable=False)  # blood_pressure, heart_rate, weight, etc.
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)  # mmHg, bpm, kg, etc.
    additional_notes = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # For blood pressure, we need systolic and diastolic values
    systolic = db.Column(db.Float)  # For blood pressure only
    diastolic = db.Column(db.Float)  # For blood pressure only

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)
    health_metrics = db.relationship('HealthMetric', backref='user', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregiver.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Caregiver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hourly_rate = db.Column(db.Float, nullable=False)
    experience_years = db.Column(db.Integer)
    specializations = db.Column(db.Text)
    verification_status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviews = db.relationship('Review', backref='caregiver', lazy=True)
    
    @property
    def average_rating(self):
        reviews = self.reviews
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_time = db.Column(db.DateTime, nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    task_type = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class EmergencyContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    elderly_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    relationship = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Call(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.String(100), unique=True, nullable=False)
    caller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    callee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='initiated')  # initiated, active, ended, missed
    
    caller = db.relationship('User', foreign_keys=[caller_id], backref='outgoing_calls')
    callee = db.relationship('User', foreign_keys=[callee_id], backref='incoming_calls')

# Initialize SocketIO after creating Flask app
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory storage for active calls
active_calls = {}
user_sid_mapping = {}  # Maps user_id to socket ID

# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    """Handle new WebSocket connections"""
    try:
        # Get user from token in request headers
        current_user = get_current_user()
        if not current_user:
            return False  # Reject connection if not authenticated
        
        # Store user's socket ID
        user_sid_mapping[current_user.id] = request.sid
        print(f'User {current_user.id} connected with socket ID: {request.sid}')
        return True
    except Exception as e:
        print(f"Connection error: {str(e)}")
        return False

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnections"""
    try:
        current_user = get_current_user()
        if current_user and current_user.id in user_sid_mapping:
            # Clean up any active calls
            for room_id, call_data in active_calls.items():
                if current_user.id in [call_data['caller_id'], call_data['callee_id']]:
                    end_call(room_id)
            
            del user_sid_mapping[current_user.id]
            print(f'User {current_user.id} disconnected')
    except Exception as e:
        print(f"Disconnection error: {str(e)}")

@socketio.on('join_call')
def handle_join_call(data):
    """Handle user joining a call"""
    try:
        room_id = data['room_id']
        current_user = get_current_user()
        
        if not room_id or not current_user:
            return
        
        call = Call.query.filter_by(room_id=room_id).first()
        if not call:
            return
        
        # Verify user is part of the call
        if current_user.id not in [call.caller_id, call.callee_id]:
            return
        
        join_room(room_id)
        active_calls[room_id] = {
            'caller_id': call.caller_id,
            'callee_id': call.callee_id,
            'status': 'active'
        }
        
        call.status = 'active'
        db.session.commit()
        
        emit('user_joined', {
            'user_id': current_user.id,
            'room_id': room_id
        }, room=room_id)
        
    except Exception as e:
        print(f"Join call error: {str(e)}")

@socketio.on('leave_call')
def handle_leave_call(data):
    """Handle user leaving a call"""
    try:
        room_id = data['room_id']
        current_user = get_current_user()
        
        if room_id in active_calls:
            end_call(room_id)
            
        leave_room(room_id)
        emit('user_left', {
            'user_id': current_user.id,
            'room_id': room_id
        }, room=room_id)
        
    except Exception as e:
        print(f"Leave call error: {str(e)}")

@socketio.on('offer')
def handle_offer(data):
    """Relay WebRTC offer to the other user"""
    try:
        room_id = data['room_id']
        emit('offer', {
            'sdp': data['sdp'],
            'room_id': room_id,
            'user_id': get_current_user().id
        }, room=room_id)
    except Exception as e:
        print(f"Offer error: {str(e)}")

@socketio.on('answer')
def handle_answer(data):
    """Relay WebRTC answer to the other user"""
    try:
        room_id = data['room_id']
        emit('answer', {
            'sdp': data['sdp'],
            'room_id': room_id,
            'user_id': get_current_user().id
        }, room=room_id)
    except Exception as e:
        print(f"Answer error: {str(e)}")

@socketio.on('ice_candidate')
def handle_ice_candidate(data):
    """Relay ICE candidates to the other user"""
    try:
        room_id = data['room_id']
        emit('ice_candidate', {
            'candidate': data['candidate'],
            'room_id': room_id,
            'user_id': get_current_user().id
        }, room=room_id)
    except Exception as e:
        print(f"ICE candidate error: {str(e)}")

# Helper Functions
def end_call(room_id):
    """End a call and update database records"""
    try:
        call = Call.query.filter_by(room_id=room_id).first()
        if call:
            call.status = 'ended'
            call.end_time = datetime.utcnow()
            db.session.commit()
        
        if room_id in active_calls:
            del active_calls[room_id]
    except Exception as e:
        print(f"End call error: {str(e)}")

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print("Received registration data:", data)  # Debug print

        # Validate required fields
        required_fields = ['email', 'password', 'user_type', 'name', 'phone']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        user = User(
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            user_type=data['user_type'],
            name=data['name'],
            phone=data['phone']
        )
        
        db.session.add(user)
        db.session.commit()
        
        try:
            send_welcome_email(user)
        except Exception as e:
            print("Email sending failed:", str(e))  # Don't fail registration if email fails
        
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'user_type': user.user_type
            },
            'token': str(user.id)  # In production, use proper JWT token
        }), 201

    except Exception as e:
        print("Registration error:", str(e))  # Debug print
        db.session.rollback()
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print("Received login data:", data)  # Debug print

        # Validate required fields
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password are required'}), 400

        user = User.query.filter_by(email=data['email']).first()
        
        if user and check_password_hash(user.password_hash, data['password']):
            return jsonify({
                'message': 'Logged in successfully',
                'token': str(user.id),  # In production, use proper JWT token
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'user_type': user.user_type
                }
            })
        
        return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        print("Login error:", str(e))  # Debug print
        return jsonify({'error': 'Login failed', 'details': str(e)}), 500
    
# Caregiver Profile and Review Routes
@app.route('/api/caregivers/profile', methods=['GET', 'POST'])
@api_login_required
def caregiver_profile():
    current_user = get_current_user()
    
    if request.method == 'GET':
        profile = Caregiver.query.filter_by(user_id=current_user.id).first()
        if not profile:
            return jsonify({'error': 'Caregiver profile not found'}), 404
            
        return jsonify({
            'id': profile.id,
            'hourly_rate': profile.hourly_rate,
            'experience_years': profile.experience_years,
            'specializations': profile.specializations,
            'verification_status': profile.verification_status,
            'name': current_user.name,
            'phone': current_user.phone,
            'average_rating': profile.average_rating
        })
    
    else:  # POST
        if current_user.user_type != 'caregiver':
            return jsonify({'error': 'Only caregivers can create profiles'}), 403
            
        data = request.get_json()
        
        profile = Caregiver.query.filter_by(user_id=current_user.id).first()
        if profile:
            # Update existing profile
            profile.hourly_rate = data['hourly_rate']
            profile.experience_years = data['experience_years']
            profile.specializations = data['specializations']
        else:
            # Create new profile
            profile = Caregiver(
                user_id=current_user.id,
                hourly_rate=data['hourly_rate'],
                experience_years=data['experience_years'],
                specializations=data['specializations'],
                verification_status=False
            )
            db.session.add(profile)
            
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully', 'id': profile.id}), 200

@app.route('/api/caregivers/<int:caregiver_id>/reviews', methods=['POST'])
@api_login_required
def create_review(caregiver_id):
    current_user = get_current_user()
    data = request.get_json()
    
    # Validate rating
    rating = data.get('rating')
    if not rating or not (1 <= rating <= 5):
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
    # Check if user has already reviewed this caregiver
    existing_review = Review.query.filter_by(
        caregiver_id=caregiver_id,
        reviewer_id=current_user.id
    ).first()
    
    if existing_review:
        return jsonify({'error': 'You have already reviewed this caregiver'}), 400
        
    review = Review(
        caregiver_id=caregiver_id,
        reviewer_id=current_user.id,
        rating=rating,
        comment=data.get('comment', '')
    )
    
    db.session.add(review)
    db.session.commit()
    
    return jsonify({
        'message': 'Review added successfully',
        'review': {
            'id': review.id,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at.isoformat()
        }
    }), 201

@app.route('/api/caregivers/search', methods=['GET'])
@api_login_required
def search_caregivers():
    # Get search parameters
    max_rate = request.args.get('max_rate', type=float)
    min_experience = request.args.get('min_experience', type=int)
    min_rating = request.args.get('min_rating', type=float)
    specialization = request.args.get('specialization')
    verified_only = request.args.get('verified_only', type=bool, default=False)
    sort_by = request.args.get('sort_by', 'rating')  # rating, price, experience
    
    # Start with base query
    query = db.session.query(Caregiver, User).join(User)
    
    # Apply filters
    if max_rate:
        query = query.filter(Caregiver.hourly_rate <= max_rate)
    if min_experience:
        query = query.filter(Caregiver.experience_years >= min_experience)
    if specialization:
        query = query.filter(Caregiver.specializations.like(f'%{specialization}%'))
    if verified_only:
        query = query.filter(Caregiver.verification_status == True)
    
    caregivers = query.all()
    
    # Post-process to include ratings and apply rating filter
    result = []
    for caregiver in caregivers:
        avg_rating = caregiver.Caregiver.average_rating
        if min_rating and avg_rating < min_rating:
            continue
            
        result.append({
            'id': caregiver.Caregiver.id,
            'name': caregiver.User.name,
            'phone': caregiver.User.phone,
            'hourly_rate': caregiver.Caregiver.hourly_rate,
            'experience_years': caregiver.Caregiver.experience_years,
            'specializations': caregiver.Caregiver.specializations,
            'verification_status': caregiver.Caregiver.verification_status,
            'average_rating': avg_rating,
            'total_reviews': len(caregiver.Caregiver.reviews)
        })
    
    # Sort results
    if sort_by == 'rating':
        result.sort(key=lambda x: x['average_rating'], reverse=True)
    elif sort_by == 'price':
        result.sort(key=lambda x: x['hourly_rate'])
    elif sort_by == 'experience':
        result.sort(key=lambda x: x['experience_years'], reverse=True)
    
    return jsonify(result)

@app.route('/api/caregivers/<int:caregiver_id>/rating', methods=['GET'])
@api_login_required
def get_rating_summary(caregiver_id):
    reviews = Review.query.filter_by(caregiver_id=caregiver_id).all()
    
    if not reviews:
        return jsonify({
            'average_rating': 0,
            'total_reviews': 0,
            'rating_distribution': {str(i): 0 for i in range(1, 6)}
        })
    
    # Calculate rating distribution
    distribution = {str(i): 0 for i in range(1, 6)}
    for review in reviews:
        distribution[str(review.rating)] += 1
    
    return jsonify({
        'average_rating': sum(r.rating for r in reviews) / len(reviews),
        'total_reviews': len(reviews),
        'rating_distribution': distribution
    })

# Task Management Routes
@app.route('/api/tasks', methods=['GET'])
@api_login_required
def get_tasks():
    current_user = get_current_user()
    # For elderly users: get their own tasks
    # For family/caregivers: get tasks of associated elderly users
    if current_user.user_type == 'elderly':
        tasks = Task.query.filter_by(user_id=current_user.id).all()
    else:
        # TODO: Implement logic to get tasks for associated elderly users
        tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_time': task.due_time.isoformat(),
        'is_completed': task.is_completed,
        'task_type': task.task_type
    } for task in tasks])

@app.route('/api/tasks', methods=['POST'])
@api_login_required
def create_task():
    current_user = get_current_user()
    data = request.get_json()
    
    task = Task(
        user_id=data.get('user_id', current_user.id),  # Allow creating tasks for other users
        title=data['title'],
        description=data.get('description', ''),
        due_time=datetime.fromisoformat(data['due_time']),
        task_type=data['task_type'],
        is_completed=False
    )
    
    db.session.add(task)
    db.session.commit()
    send_task_reminder_email(User.query.get(task.user_id), task)
    
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_time': task.due_time.isoformat(),
        'is_completed': task.is_completed,
        'task_type': task.task_type
    }), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@api_login_required
def update_task(task_id):
    current_user = get_current_user()
    task = Task.query.get_or_404(task_id)
    
    # Check if user has permission to update this task
    if task.user_id != current_user.id and current_user.user_type not in ['family', 'caregiver']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.due_time = datetime.fromisoformat(data['due_time']) if 'due_time' in data else task.due_time
    task.is_completed = data.get('is_completed', task.is_completed)
    task.task_type = data.get('task_type', task.task_type)
    
    db.session.commit()
    
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_time': task.due_time.isoformat(),
        'is_completed': task.is_completed,
        'task_type': task.task_type
    })

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@api_login_required
def delete_task(task_id):
    current_user = get_current_user()
    task = Task.query.get_or_404(task_id)
    
    # Check if user has permission to delete this task
    if task.user_id != current_user.id and current_user.user_type not in ['family', 'caregiver']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'message': 'Task deleted successfully'})

@app.route('/api/tasks/upcoming', methods=['GET'])
@api_login_required
def get_upcoming_tasks():
    current_user = get_current_user()
    # Get tasks due in the next 24 hours
    upcoming_tasks = Task.query.filter(
        Task.user_id == current_user.id,
        Task.due_time >= datetime.utcnow(),
        Task.due_time <= datetime.utcnow() + timedelta(days=1),
        Task.is_completed == False
    ).order_by(Task.due_time).all()
    
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_time': task.due_time.isoformat(),
        'task_type': task.task_type
    } for task in upcoming_tasks])

# Emergency Alert System Routes
@app.route('/api/emergency/contacts', methods=['GET'])
@api_login_required
def get_emergency_contacts():
    current_user = get_current_user()
    contacts = EmergencyContact.query.filter_by(elderly_id=current_user.id).all()
    
    return jsonify([{
        'id': contact.id,
        'contact_user': User.query.get(contact.contact_id).name,
        'phone': User.query.get(contact.contact_id).phone,
        'relationship': contact.relationship
    } for contact in contacts])

@app.route('/api/emergency/contacts', methods=['POST'])
@api_login_required
def add_emergency_contact():
    current_user = get_current_user()
    data = request.get_json()
    
    # First create a user account for the emergency contact if they don't exist
    contact_user = User.query.filter_by(email=data['email']).first()
    if not contact_user:
        contact_user = User(
            email=data['email'],
            password_hash=generate_password_hash('temporary_password'),  # They should reset this
            user_type='family',
            name=data['name'],
            phone=data['phone']
        )
        db.session.add(contact_user)
        db.session.commit()
    
    # Create emergency contact relationship
    contact = EmergencyContact(
        elderly_id=current_user.id,
        contact_id=contact_user.id,
        relationship=data['relationship']
    )
    
    db.session.add(contact)
    db.session.commit()
    
    return jsonify({
        'message': 'Emergency contact added successfully',
        'contact': {
            'id': contact.id,
            'name': contact_user.name,
            'phone': contact_user.phone,
            'relationship': contact.relationship
        }
    }), 201

@app.route('/api/emergency/alert', methods=['POST'])
@api_login_required
def create_emergency_alert():
    current_user = get_current_user()
    data = request.get_json()
    
    # Get all emergency contacts
    contacts = EmergencyContact.query.filter_by(elderly_id=current_user.id).all()
    
    if not contacts:
        return jsonify({'error': 'No emergency contacts found'}), 400
    
    # In a real application, you would:
    # 1. Send SMS notifications
    # 2. Make automated phone calls
    # 3. Send push notifications
    # 4. Contact emergency services if configured
    
    # For now, we'll simulate the alert
    alert_message = {
        'type': 'EMERGENCY_ALERT',
        'elderly_name': current_user.name,
        'elderly_phone': current_user.phone,
        'message': data.get('message', 'Emergency assistance needed!'),
        'location': data.get('location', 'Location not provided'),
        'timestamp': datetime.utcnow().isoformat(),
        'notified_contacts': [{
            'name': User.query.get(contact.contact_id).name,
            'phone': User.query.get(contact.contact_id).phone
        } for contact in contacts]
    }

    send_emergency_alert_email(
        emergency_contacts=contacts,
        alert_message=alert_message['message'],
        elderly_user=current_user
    )
    
    return jsonify({
        'message': 'Emergency alert sent successfully',
        'alert': alert_message
    })

@app.route('/api/emergency/test', methods=['POST'])
@api_login_required
def test_emergency_system():
    """Test the emergency alert system without notifying contacts"""
    current_user = get_current_user()
    
    contacts = EmergencyContact.query.filter_by(elderly_id=current_user.id).all()
    if not contacts:
        return jsonify({'error': 'No emergency contacts found'}), 400
    
    return jsonify({
        'message': 'Emergency system test successful',
        'contacts_count': len(contacts),
        'system_status': 'operational'
    })

@app.route('/api/caregivers/top', methods=['GET'])
@api_login_required
def get_top_caregivers():
    """Get top-rated and verified caregivers"""
    top_caregivers = db.session.query(Caregiver, User)\
        .join(User)\
        .filter(Caregiver.verification_status == True)\
        .order_by(Caregiver.experience_years.desc())\
        .limit(5)\
        .all()
    
    return jsonify([{
        'id': caregiver.Caregiver.id,
        'name': caregiver.User.name,
        'hourly_rate': caregiver.Caregiver.hourly_rate,
        'experience_years': caregiver.Caregiver.experience_years,
        'specializations': caregiver.Caregiver.specializations,
        'average_rating': caregiver.Caregiver.average_rating
    } for caregiver in top_caregivers])

@app.route('/api/caregivers/<int:caregiver_id>/reviews', methods=['GET'])
@api_login_required
def get_reviews(caregiver_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    reviews = Review.query.filter_by(caregiver_id=caregiver_id)\
        .order_by(Review.created_at.desc())\
        .paginate(page=page, per_page=per_page)
    
    return jsonify({
        'total_reviews': reviews.total,
        'current_page': reviews.page,
        'total_pages': reviews.pages,
        'reviews': [{
            'id': review.id,
            'rating': review.rating,
            'comment': review.comment,
            'reviewer_name': User.query.get(review.reviewer_id).name,
            'created_at': review.created_at.isoformat()
        } for review in reviews.items]
    })

@app.route('/api/caregivers/<int:caregiver_id>/contact', methods=['POST'])
@api_login_required
def contact_caregiver(caregiver_id):
    current_user = get_current_user()
    caregiver = Caregiver.query.get_or_404(caregiver_id)
    caregiver_user = User.query.get(caregiver.user_id)
    
    # In production, you would:
    # 1. Create a chat/messaging system
    # 2. Send email/SMS notification
    # 3. Create a connection request
    
    return jsonify({
        'message': 'Contact request sent successfully',
        'caregiver': {
            'name': caregiver_user.name,
            'phone': caregiver_user.phone
        }
    })

# Health Metrics Routes
@app.route('/api/health/metrics', methods=['POST'])
@api_login_required
def log_health_metric():
    current_user = get_current_user()
    data = request.get_json()
    
    # Validate metric type
    valid_metrics = ['blood_pressure', 'heart_rate', 'weight', 'blood_sugar', 'temperature', 'oxygen_level']
    if data['metric_type'] not in valid_metrics:
        return jsonify({'error': f'Invalid metric type. Must be one of: {", ".join(valid_metrics)}'}), 400
    
    # Special handling for blood pressure
    if data['metric_type'] == 'blood_pressure':
        if 'systolic' not in data or 'diastolic' not in data:
            return jsonify({'error': 'Blood pressure requires both systolic and diastolic values'}), 400
            
        metric = HealthMetric(
            user_id=current_user.id,
            metric_type=data['metric_type'],
            value=0,  # Not used for blood pressure
            unit='mmHg',
            systolic=data['systolic'],
            diastolic=data['diastolic'],
            additional_notes=data.get('notes')
        )
    else:
        # Handle other metrics
        metric = HealthMetric(
            user_id=current_user.id,
            metric_type=data['metric_type'],
            value=data['value'],
            unit=data['unit'],
            additional_notes=data.get('notes')
        )
    
    db.session.add(metric)
    db.session.commit()
    
    return jsonify({
        'message': 'Health metric logged successfully',
        'metric_id': metric.id
    }), 201

@app.route('/api/health/metrics', methods=['GET'])
@api_login_required
def get_health_metrics():
    current_user = get_current_user()
    metric_type = request.args.get('type')
    days = request.args.get('days', type=int, default=7)
    
    # Base query
    query = HealthMetric.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    if metric_type:
        query = query.filter_by(metric_type=metric_type)
    if days:
        since_date = datetime.utcnow() - timedelta(days=days)
        query = query.filter(HealthMetric.timestamp >= since_date)
    
    metrics = query.order_by(HealthMetric.timestamp.desc()).all()
    
    return jsonify([{
        'id': metric.id,
        'type': metric.metric_type,
        'value': metric.value if metric.metric_type != 'blood_pressure' else None,
        'systolic': metric.systolic if metric.metric_type == 'blood_pressure' else None,
        'diastolic': metric.diastolic if metric.metric_type == 'blood_pressure' else None,
        'unit': metric.unit,
        'notes': metric.additional_notes,
        'timestamp': metric.timestamp.isoformat()
    } for metric in metrics])

@app.route('/api/health/summary', methods=['GET'])
@api_login_required
def get_health_summary():
    current_user = get_current_user()
    days = request.args.get('days', type=int, default=7)
    since_date = datetime.utcnow() - timedelta(days=days)
    
    # Get metrics for the specified period
    metrics = HealthMetric.query.filter(
        HealthMetric.user_id == current_user.id,
        HealthMetric.timestamp >= since_date
    ).all()
    
    # Group metrics by type
    summary = {}
    for metric in metrics:
        if metric.metric_type not in summary:
            summary[metric.metric_type] = {
                'count': 0,
                'values': [],
                'unit': metric.unit
            }
        
        summary[metric.metric_type]['count'] += 1
        if metric.metric_type == 'blood_pressure':
            summary[metric.metric_type]['values'].append({
                'systolic': metric.systolic,
                'diastolic': metric.diastolic,
                'timestamp': metric.timestamp.isoformat()
            })
        else:
            summary[metric.metric_type]['values'].append({
                'value': metric.value,
                'timestamp': metric.timestamp.isoformat()
            })
    
    # Calculate statistics for each metric type
    for metric_type, data in summary.items():
        if metric_type == 'blood_pressure':
            systolic_values = [v['systolic'] for v in data['values']]
            diastolic_values = [v['diastolic'] for v in data['values']]
            
            data['statistics'] = {
                'systolic': {
                    'avg': sum(systolic_values) / len(systolic_values),
                    'min': min(systolic_values),
                    'max': max(systolic_values)
                },
                'diastolic': {
                    'avg': sum(diastolic_values) / len(diastolic_values),
                    'min': min(diastolic_values),
                    'max': max(diastolic_values)
                }
            }
        else:
            values = [v['value'] for v in data['values']]
            data['statistics'] = {
                'avg': sum(values) / len(values),
                'min': min(values),
                'max': max(values)
            }
    
    return jsonify({
        'period_days': days,
        'metrics': summary
    })

@app.route('/api/health/alerts', methods=['GET'])
@api_login_required
def check_health_alerts():
    current_user = get_current_user()
    
    # Define normal ranges for different metrics
    normal_ranges = {
        'blood_pressure': {
            'systolic': {'min': 90, 'max': 140},
            'diastolic': {'min': 60, 'max': 90}
        },
        'heart_rate': {'min': 60, 'max': 100},
        'blood_sugar': {'min': 70, 'max': 140},
        'temperature': {'min': 36.1, 'max': 37.2},
        'oxygen_level': {'min': 95, 'max': 100}
    }
    
    # Get latest metrics
    alerts = []
    for metric_type, ranges in normal_ranges.items():
        latest_metric = HealthMetric.query.filter_by(
            user_id=current_user.id,
            metric_type=metric_type
        ).order_by(HealthMetric.timestamp.desc()).first()
        
        if latest_metric:
            if metric_type == 'blood_pressure':
                if (latest_metric.systolic < ranges['systolic']['min'] or 
                    latest_metric.systolic > ranges['systolic']['max'] or
                    latest_metric.diastolic < ranges['diastolic']['min'] or
                    latest_metric.diastolic > ranges['diastolic']['max']):
                    alerts.append({
                        'metric_type': metric_type,
                        'message': f'Blood pressure reading ({latest_metric.systolic}/{latest_metric.diastolic}) is outside normal range',
                        'timestamp': latest_metric.timestamp.isoformat()
                    })
            else:
                if latest_metric.value < ranges['min'] or latest_metric.value > ranges['max']:
                    alerts.append({
                        'metric_type': metric_type,
                        'message': f'{metric_type.replace("_", " ").title()} reading ({latest_metric.value}) is outside normal range',
                        'timestamp': latest_metric.timestamp.isoformat()
                    })
    
    # Add this block here - Send email if there are any alerts
    if len(alerts) > 0:
        try:
            send_health_alert_email(current_user, alerts[0])  # Send alert for the first detected issue
        except Exception as e:
            # Log the error but don't prevent the API from returning alerts
            print(f"Failed to send health alert email: {str(e)}")
    
    return jsonify({
        'has_alerts': len(alerts) > 0,
        'alerts': alerts
    })

@app.route('/api/test/email', methods=['POST'])
@api_login_required
def test_email():
    """Test endpoint to verify email functionality"""
    try:
        send_welcome_email(request.user)
        return jsonify({'message': 'Test email queued successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API Routes
@app.route('/api/calls/start', methods=['POST'])
@api_login_required
def start_call():
    """Initiate a new call"""
    try:
        data = request.get_json()
        callee_id = data.get('callee_id')
        
        if not callee_id:
            return jsonify({'error': 'Callee ID is required'}), 400
            
        # Verify callee exists
        callee = User.query.get(callee_id)
        if not callee:
            return jsonify({'error': 'Invalid callee ID'}), 404
            
        # Generate unique room ID
        room_id = f"call_{request.user.id}_{callee_id}_{int(datetime.utcnow().timestamp())}"
        
        # Create call record
        call = Call(
            room_id=room_id,
            caller_id=request.user.id,
            callee_id=callee_id
        )
        
        db.session.add(call)
        db.session.commit()
        
        # Notify callee if they're online
        if callee_id in user_sid_mapping:
            emit('incoming_call', {
                'room_id': room_id,
                'caller_id': request.user.id,
                'caller_name': request.user.name
            }, room=user_sid_mapping[callee_id])
        
        return jsonify({
            'room_id': room_id,
            'caller_id': request.user.id,
            'callee_id': callee_id,
            'status': 'initiated'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/calls/history', methods=['GET'])
@api_login_required
def get_call_history():
    """Get user's call history"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        calls = Call.query.filter(
            db.or_(
                Call.caller_id == request.user.id,
                Call.callee_id == request.user.id
            )
        ).order_by(Call.start_time.desc()).paginate(page=page, per_page=per_page)
        
        return jsonify({
            'total_calls': calls.total,
            'current_page': calls.page,
            'total_pages': calls.pages,
            'calls': [{
                'id': call.id,
                'room_id': call.room_id,
                'caller_name': call.caller.name,
                'callee_name': call.callee.name,
                'start_time': call.start_time.isoformat(),
                'end_time': call.end_time.isoformat() if call.end_time else None,
                'status': call.status
            } for call in calls.items]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    socketio.run(app, debug=True)       