#!/usr/bin/env python3
"""
Test script for Spy Cat Agency API
Run this script to verify all endpoints are working correctly
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api():
    print("Testing Spy Cat Agency API...")
    
    print("\n1. Testing health check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    print("\n2. Creating spy cat...")
    cat_data = {
        "name": "Shadow",
        "years_of_experience": 3,
        "breed": "Siamese",
        "salary": 45000
    }
    response = requests.post(f"{BASE_URL}/spy-cats/", json=cat_data)
    print(f"Status: {response.status_code}")
    cat = response.json()
    print(f"Created cat: {cat}")
    cat_id = cat["id"]
    
    print("\n3. Listing spy cats...")
    response = requests.get(f"{BASE_URL}/spy-cats/")
    print(f"Status: {response.status_code}")
    cats = response.json()
    print(f"Total cats: {len(cats)}")
    
    print("\n4. Creating mission...")
    mission_data = {
        "targets": [
            {
                "name": "John Doe",
                "country": "USA"
            },
            {
                "name": "Jane Smith",
                "country": "Canada"
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/missions/", json=mission_data)
    print(f"Status: {response.status_code}")
    mission = response.json()
    print(f"Created mission: {mission}")
    mission_id = mission["id"]
    target_id = mission["targets"][0]["id"]
    
    print("\n5. Assigning cat to mission...")
    assign_data = {"cat_id": cat_id}
    response = requests.put(f"{BASE_URL}/missions/{mission_id}/assign", json=assign_data)
    print(f"Status: {response.status_code}")
    mission = response.json()
    print(f"Assigned mission: {mission}")
    
    print("\n6. Updating target notes...")
    target_update = {
        "notes": "Target spotted at downtown cafe. Meeting with unknown contact.",
        "is_completed": False
    }
    response = requests.put(f"{BASE_URL}/targets/{target_id}", json=target_update)
    print(f"Status: {response.status_code}")
    target = response.json()
    print(f"Updated target: {target}")
    
    print("\n7. Marking target as complete...")
    target_update = {"is_completed": True}
    response = requests.put(f"{BASE_URL}/targets/{target_id}", json=target_update)
    print(f"Status: {response.status_code}")
    target = response.json()
    print(f"Completed target: {target}")
    
    print("\n8. Checking mission completion...")
    response = requests.get(f"{BASE_URL}/missions/{mission_id}")
    print(f"Status: {response.status_code}")
    mission = response.json()
    print(f"Mission status: {mission}")
    
    print("\n9. Updating cat salary...")
    salary_update = {"salary": 50000}
    response = requests.put(f"{BASE_URL}/spy-cats/{cat_id}", json=salary_update)
    print(f"Status: {response.status_code}")
    cat = response.json()
    print(f"Updated cat: {cat}")
    
    print("\nAll tests completed successfully!")
    print(f"Cat ID: {cat_id}")
    print(f"Mission ID: {mission_id}")
    print(f"Target ID: {target_id}")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API.")
        print("Make sure the server is running on http://localhost:8000")
        print("Run: python main.py")
    except Exception as e:
        print(f"Error: {e}")