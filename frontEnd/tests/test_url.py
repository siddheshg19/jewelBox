# frontEnd/tests/test_urls.py

from django.urls import reverse, resolve

class TestUrls:
    """Groups URL related tests."""

    def test_login_url_resolves(self):
        """
        Test Case Type: URL Test
        Goal: Verify that the URL path generated for the name 'login'
              correctly maps (resolves) to the view function/class associated
              with the name 'login'.
        """
        # Assumes you have a URL pattern named 'login' in your urls.py
        url_name = 'login'
        path = reverse(url_name)
        print(f"\n[URL Test] Reversed path for '{url_name}': {path}") # Added print statement

        resolved_view_name = resolve(path).view_name
        print(f"[URL Test] Path '{path}' resolved to view name: '{resolved_view_name}'") # Added print statement

        # Check if the resolved view name matches the expected URL name
        assert resolved_view_name == url_name

        print("[URL Test] Login URL resolution test PASSED") # Added print statement