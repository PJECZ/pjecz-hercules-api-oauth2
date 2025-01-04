"""
Unit Tests Autoridades
"""

import unittest

import requests

from tests import config, oauth2_token


class TestAutoridades(unittest.TestCase):
    """Tests Autoridades class"""

    def test_get_autoridades(self):
        """Test get autoridades"""
        try:
            response = requests.get(
                url=f"{config['base_url']}/api/v1/autoridades",
                headers={"Authorization": f"Bearer {oauth2_token}"},
                timeout=config["timeout"],
            )
        except requests.exceptions.RequestException as error:
            self.fail(error)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
