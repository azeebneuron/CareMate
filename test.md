IMPLEMENTED FEATURES:

1. User Authentication System:
```bash
# Register a new user
curl -X POST http://localhost:5000/api/auth/register \
-H "Content-Type: application/json" \
-d '{
    "email": "elderly@example.com",
    "password": "password123",
    "user_type": "elderly",
    "name": "John Doe",
    "phone": "1234567890"
}'

# Register a caregiver
curl -X POST http://localhost:5000/api/auth/register \
-H "Content-Type: application/json" \
-d '{
    "email": "caregiver@example.com",
    "password": "password123",
    "user_type": "caregiver",
    "name": "Jane Smith",
    "phone": "0987654321"
}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
-H "Content-Type: application/json" \
-d '{
    "email": "elderly@example.com",
    "password": "password123"
}'
```

2. Task Management System:
```bash
# Create task
curl -X POST http://localhost:5000/api/tasks \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_TOKEN" \
-d '{
    "title": "Take Medicine",
    "description": "Take blood pressure medicine",
    "due_time": "2024-12-29T10:00:00",
    "task_type": "medication"
}'

# Get all tasks
curl http://localhost:5000/api/tasks \
-H "Authorization: Bearer YOUR_TOKEN"

# Get upcoming tasks
curl http://localhost:5000/api/tasks/upcoming \
-H "Authorization: Bearer YOUR_TOKEN"

# Update task
curl -X PUT http://localhost:5000/api/tasks/1 \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_TOKEN" \
-d '{
    "is_completed": true,
    "due_time": "2024-12-29T10:00:00"
}'

# Delete task
curl -X DELETE http://localhost:5000/api/tasks/1 \
-H "Authorization: Bearer YOUR_TOKEN"
```

3. Emergency Alert System:
```bash
# Add emergency contact
curl -X POST http://localhost:5000/api/emergency/contacts \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_TOKEN" \
-d '{
    "name": "Emergency Contact",
    "email": "emergency@example.com",
    "phone": "1122334455",
    "relationship": "son"
}'

# Get emergency contacts
curl http://localhost:5000/api/emergency/contacts \
-H "Authorization: Bearer YOUR_TOKEN"

# Send emergency alert
curl -X POST http://localhost:5000/api/emergency/alert \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_TOKEN" \
-d '{
    "message": "Need immediate assistance",
    "location": "Bedroom"
}'

# Test emergency system
curl -X POST http://localhost:5000/api/emergency/test \
-H "Authorization: Bearer YOUR_TOKEN"
```

4. Caregiver Marketplace:
```bash
# Create caregiver profile
curl -X POST http://localhost:5000/api/caregivers/profile \
-H "Content-Type: application/json" \
-H "Authorization: Bearer CAREGIVER_TOKEN" \
-d '{
    "hourly_rate": 25.0,
    "experience_years": 5,
    "specializations": "Elder care, Dementia care"
}'

# Search caregivers
curl "http://localhost:5000/api/caregivers/search?max_rate=30&min_experience=3" \
-H "Authorization: Bearer YOUR_TOKEN"

# Get top caregivers
curl http://localhost:5000/api/caregivers/top \
-H "Authorization: Bearer YOUR_TOKEN"

# Add review
curl -X POST http://localhost:5000/api/caregivers/1/reviews \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_TOKEN" \
-d '{
    "rating": 5,
    "comment": "Excellent care and very professional"
}'

# Get reviews
curl http://localhost:5000/api/caregivers/1/reviews \
-H "Authorization: Bearer YOUR_TOKEN"

# Contact caregiver
curl -X POST http://localhost:5000/api/caregivers/1/contact \
-H "Authorization: Bearer YOUR_TOKEN"
```

5. Health Metrics System:
```bash
# Log blood pressure
curl -X POST http://localhost:5000/api/health/metrics \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_TOKEN" \
-d '{
    "metric_type": "blood_pressure",
    "systolic": 120,
    "diastolic": 80,
    "notes": "Morning reading"
}'

# Log heart rate
curl -X POST http://localhost:5000/api/health/metrics \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_TOKEN" \
-d '{
    "metric_type": "heart_rate",
    "value": 75,
    "unit": "bpm",
    "notes": "After walking"
}'

# Get health metrics
curl "http://localhost:5000/api/health/metrics?days=7" \
-H "Authorization: Bearer YOUR_TOKEN"

# Get health summary
curl http://localhost:5000/api/health/summary \
-H "Authorization: Bearer YOUR_TOKEN"

# Check health alerts
curl http://localhost:5000/api/health/alerts \
-H "Authorization: Bearer YOUR_TOKEN"

# Testing Videocall
# Get a token by logging in first
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password"
  }'

# Start a call (replace TOKEN and CALLEE_ID)
curl -X POST http://localhost:5000/api/calls/start \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "callee_id": "CALLEE_ID"
  }'
```

The callee_id would be the user ID of the person you want to call.

Check call history
```bash
curl -X GET http://localhost:5000/api/calls/history \
  -H "Authorization: Bearer TOKEN"
```

MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') ,

This has also been used, so just add MAIL_USERNAME AND MAIL_PASSWORD in a .env file after creating account in mailtrap and connecting it to flask mail

## Testing Mail requires setting up Mailtrap account and using a .env file