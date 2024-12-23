import requests
import json

BASE_URL = "https://social-media-alx-project.onrender.com/api"

def test_authentication():
    # 1. First, try to register a new user
    register_url = f"{BASE_URL}/auth/register/"
    register_data = {
        "username": "testuser2",  # Changed username to avoid conflict
        "email": "testuser2@example.com",
        "password": "testpass123",
        "password2": "testpass123"
    }
    
    print("\n1. Testing Registration:")
    try:
        response = requests.post(register_url, json=register_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Registration Error: {str(e)}")

    # 2. Then, get a token using login
    token_url = f"{BASE_URL}/auth/token/"
    token_data = {
        "username": "testuser",  # Using existing user
        "password": "testpass123"
    }
    
    print("\n2. Getting Token:")
    try:
        response = requests.post(token_url, json=token_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            access_token = response.json().get('access')
            
            # 3. Test accessing users endpoint with token
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            
            print("\n3. Testing Users Endpoint With Token:")
            users_url = f"{BASE_URL}/users/"
            response = requests.get(users_url, headers=headers)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            # 4. Test accessing users endpoint without token
            print("\n4. Testing Users Endpoint Without Token:")
            response = requests.get(users_url)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            # 5. Test creating a post (protected endpoint)
            print("\n5. Testing Post Creation With Token:")
            posts_url = f"{BASE_URL}/posts/"
            post_data = {
                "content": "Test post from API",
                "visibility": "public"
            }
            response = requests.post(posts_url, json=post_data, headers=headers)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            # 6. Test creating a post without token
            print("\n6. Testing Post Creation Without Token:")
            response = requests.post(posts_url, json=post_data)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            # 7. Test viewing posts (should work without token)
            print("\n7. Testing Viewing Posts Without Token:")
            response = requests.get(posts_url)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
    except Exception as e:
        print(f"Token/Access Error: {str(e)}")

if __name__ == "__main__":
    test_authentication()
