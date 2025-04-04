# frontEnd/tests/test_views.py

import pytest
from django.urls import reverse
# Use get_user_model for better practice, though CustomUser works if it's THE user model
# from django.contrib.auth import get_user_model
from jewelBoxDbServices.models import CustomUser, Jewelry # Import necessary models
# Import SimpleUploadedFile
from django.core.files.uploadedfile import SimpleUploadedFile

# pytest fixture to mark tests needing database access
pytestmark = pytest.mark.django_db

# --- Fixtures ---

@pytest.fixture
def normal_user(db):
    """Fixture to create a standard user."""
    user = CustomUser.objects.create_user(
        username='testuser@example.com',
        email='testuser@example.com',
        password='password123',
        first_name='Test',
        last_name='User',
        is_owner=False
    )
    return user

@pytest.fixture
def sample_jewelry(db):
    """Fixture to create a sample Jewelry item with a dummy image."""
    # Create a simple dummy image file in memory for the test
    # A minimal 1x1 GIF is small and usually sufficient
    dummy_image = SimpleUploadedFile(
        name='test_image.gif',
        content=b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;',
        content_type='image/gif'
    )

    jewelry = Jewelry.objects.create(
        name="Test Ring",
        description="A beautiful test ring",
        price=100.00,
        stock=10,
        category="Ring",
        image=dummy_image # Assign the dummy image here
    )
    return jewelry

# --- Basic Test Cases ---

# Test 1: Test a simple public page (GET request)
def test_home_view(client):
    """Test the home page loads correctly."""
    # Assumes 'home' is the name defined in your frontEnd/urls.py or project urls.py
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
    # Check that the correct template was used (optional but good practice)
    assert 'home.html' in [t.name for t in response.templates]

# Test 2: Test a view requiring login (GET request)
def test_jewelry_list_view_authenticated(client, normal_user, sample_jewelry):
    """Test jewelry list shows items for an authenticated user."""
    # Log in the user using pytest-django's client helper
    client.force_login(normal_user)

    # Assumes 'jewelry_list' is the name in your frontEnd/urls.py
    url = reverse('jewelry_list')
    response = client.get(url) # This line was failing

    # Assertions after the fix:
    assert response.status_code == 200 # Should now pass the render step
    assert 'jewelry_list.html' in [t.name for t in response.templates]
    # Check that the jewelry item created by the fixture is in the context
    assert 'jewelry_items' in response.context
    # Convert QuerySet to list for easier assertion if needed, or check membership
    assert sample_jewelry in response.context['jewelry_items']
    # Check that the user accessing the view is the logged-in user
    # Accessing response.context['user'] depends on how you pass context in the view
    # request.user is more reliable if the template context includes it
    assert response.wsgi_request.user == normal_user # Check user on the request

# Test 3: Test a view with a POST request (Login functionality)
def test_login_view_post_success_normal_user(client, normal_user):
    """Test successful login for a normal user redirects correctly."""
    # Assumes 'login' is the name in your frontEnd/urls.py
    url = reverse('login')
    login_data = {
        # The login view uses 'email' for the username field
        'email': 'testuser@example.com',
        'password': 'password123'
    }
    # Send a POST request to the login URL with the user's credentials
    response = client.post(url, login_data)

    # Check for a successful redirect (status code 302)
    assert response.status_code == 302
    # Check that the redirect goes to the expected page ('jewelry_list')
    assert response.url == reverse('jewelry_list')
    # Check if the user is actually authenticated in the session after the POST
    # Access the user object from the request associated with the response
    assert response.wsgi_request.user.is_authenticated
    assert response.wsgi_request.user == normal_user