#!/usr/bin/env python3
"""
Campus Event Management Platform - API Testing Script
This script demonstrates all the API endpoints and generates sample reports.
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any

class CampusEventTester:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.college_id = "CMU"
        self.headers = {"Content-Type": "application/json"}

    def make_request(self, method: str, endpoint: str, data: Dict = None) -> requests.Response:
        """Make HTTP request with error handling."""
        url = f"{self.base_url}{endpoint}"
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=self.headers, json=data)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=self.headers)

            print(f"\n{method.upper()} {endpoint}")
            if data:
                print(f"Payload: {json.dumps(data)}")
            print(f"Status: {response.status_code}")

            try:
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2)}")
            except json.JSONDecodeError:
                print(f"Response (non-JSON): {response.text}")

            return response

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def test_health_check(self):
        """Test health check endpoint."""
        print("=" * 60)
        print("1. HEALTH CHECK")
        print("=" * 60)
        self.make_request("GET", "/health")

    # Replace the existing test_create_event function with this one

    def test_create_event(self):
        """Test event creation."""
        print("\n" + "=" * 60)
        print("2. CREATE NEW HACKATHON EVENT FOR CMU")
        print("=" * 60)

        start_time = datetime.now() + timedelta(days=20)
        end_time = start_time + timedelta(days=2) # A hackathon lasts longer

        event_data = {
            "title": "AI for Good Hackathon",
            "description": "Join us for a 48-hour hackathon to build AI solutions for social challenges.",
            "event_type": "hackathon", # <--- IMPORTANT: Set the type
            "start_datetime": start_time.isoformat(),
            "end_datetime": end_time.isoformat(),
            "location": "Innovation Hall",
            "capacity": 100,
            "created_by": "admin@cmu.edu"
        }

        response = self.make_request("POST", f"/api/v1/colleges/{self.college_id}/events", event_data)
        if response and response.status_code == 201:
            return response.json().get('id')
        return None
    def test_get_events(self):
        """Test getting all events."""
        print("\n" + "=" * 60)
        print("3. GET ALL EVENTS")
        print("=" * 60)
        self.make_request("GET", f"/api/v1/colleges/{self.college_id}/events")

    def test_student_registration(self, event_id: str):
        """Test student registration."""
        print("\n" + "=" * 60)
        print("4. STUDENT REGISTRATION")
        print("=" * 60)

        # Register multiple students
        students = ["MIT-STU-001", "MIT-STU-002", "MIT-STU-003"]

        for student_id in students:
            registration_data = {"student_id": student_id}
            self.make_request("POST", f"/api/v1/colleges/{self.college_id}/events/{event_id}/register", registration_data)
            time.sleep(0.1)

        # Test duplicate registration
        print("\n--- Testing duplicate registration (expected 409) ---")
        self.make_request("POST", f"/api/v1/colleges/{self.college_id}/events/{event_id}/register", {"student_id": "MIT-STU-001"})

        # Test capacity exceeded
        print("\n--- Testing capacity exceeded (expected 409) ---")
        self.make_request("POST", f"/api/v1/colleges/STANFORD/events/{event_id}/register", {"student_id": "STANFORD-STU-001"})


    def test_mark_attendance(self, event_id: str):
        """Test attendance marking."""
        print("\n" + "=" * 60)
        print("5. MARK ATTENDANCE")
        print("=" * 60)

        # Mark attendance for registered students
        students_present = ["MIT-STU-001", "MIT-STU-002"]
        for student_id in students_present:
            attendance_data = {"student_id": student_id, "status": "present"}
            self.make_request("POST", f"/api/v1/colleges/{self.college_id}/events/{event_id}/attendance", attendance_data)
            time.sleep(0.1)

        # Test admin override for an unregistered student
        print("\n--- Testing admin override for a non-registered student ---")
        override_data = {
            "student_id": "STANFORD-STU-002",
            "admin_override": True,
            "status": "present"
        }
        self.make_request("POST", f"/api/v1/colleges/{self.college_id}/events/{event_id}/attendance", override_data)

    def test_submit_feedback(self, event_id: str):
        """Test feedback submission."""
        print("\n" + "=" * 60)
        print("6. SUBMIT FEEDBACK")
        print("=" * 60)

        feedback_data = [
            {"student_id": "MIT-STU-001", "rating": 5, "comments": "Excellent workshop!"},
            {"student_id": "MIT-STU-002", "rating": 4, "comments": "Good content."},
        ]

        for feedback in feedback_data:
            self.make_request("POST", f"/api/v1/colleges/{self.college_id}/events/{event_id}/feedback", feedback)
            time.sleep(0.1)

        # Test feedback without attendance
        print("\n--- Testing feedback without attendance (expected 403) ---")
        self.make_request("POST", f"/api/v1/colleges/{self.college_id}/events/{event_id}/feedback", {"student_id": "MIT-STU-003", "rating": 5})

        # Test invalid rating
        print("\n--- Testing invalid rating (expected 400) ---")
        self.make_request("POST", f"/api/v1/colleges/{self.college_id}/events/{event_id}/feedback", {"student_id": "MIT-STU-001", "rating": 6})

    def test_all_reports(self, event_id: str):
        """Test all reporting endpoints."""
        print("\n" + "=" * 60)
        print("7. GENERATING REPORTS")
        print("=" * 60)
        self.make_request("GET", f"/api/v1/colleges/{self.college_id}/reports/event-popularity")
        self.make_request("GET", f"/api/v1/colleges/{self.college_id}/reports/student-participation")

    def run_full_test_suite(self):
        """Run complete test suite."""
        print("🎓 Starting Campus Event Management Platform Test Suite")
        print("=" * 80)

        self.test_health_check()
        new_event_id = self.test_create_event()

        if new_event_id:
            self.test_get_events()
            self.test_student_registration(new_event_id)
            self.test_mark_attendance(new_event_id)
            self.test_submit_feedback(new_event_id)
            self.test_all_reports(new_event_id)
        else:
            print("\n[ERROR] Event creation failed. Halting test suite.")

        print("\n" + "=" * 80)
        print("🎉 Test Suite Completed!")
        print("=" * 80)

if __name__ == '__main__':
    tester = CampusEventTester()
    tester.run_full_test_suite()