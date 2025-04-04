# jewelBoxDbServices/tests/test_models.py

import pytest
from mixer.backend.django import mixer

# Import your specific model
from jewelBoxDbServices.models import Jewelry

#-----------------------------------
# Test Case for Jewelry Model __str__
#-----------------------------------

# 1. @pytest.mark.django_db
#    o This decorator tells pytest that this test interacts with the
#      database (by creating a Jewelry model instance).
#    o Without this, database-related operations (like saving
#      models via mixer.blend) would fail.
@pytest.mark.django_db
def test_jewelry_model_str():
    """
    Tests the __str__ representation of the Jewelry model.
    """
    print("\n--- Starting test_jewelry_model_str ---")

    # 2. mixer.blend('jewelBoxDbServices.Jewelry', ...)
    #    o mixer.blend() is used to create a test instance of the Jewelry
    #      model.
    #    o It automatically fills in required fields (like name, price, stock)
    #      with random or default values.
    #    o We don't need to explicitly set fields here, as __str__ only
    #      depends on 'name', which mixer provides.
    print("[Mixing] Creating Jewelry instance with mixer.blend...")
    jewelry = mixer.blend('jewelBoxDbServices.Jewelry')
    print(f"[Mixing] Jewelry instance created with name: '{jewelry.name}'")

    # 3. Assertion: assert str(jewelry) == jewelry.name
    #    o This checks whether the string representation of the jewelry
    #      object (obtained by calling str()) is equal to its 'name'
    #      attribute.
    #    o This verifies that the __str__ method in the Jewelry model is
    #      correctly implemented to return the name.
    expected_str = jewelry.name
    actual_str = str(jewelry)
    print(f"[Asserting] Checking if str(jewelry) ('{actual_str}') == jewelry.name ('{expected_str}')")
    assert actual_str == expected_str
    print("[Assertion] Passed: __str__ method returns the correct name.")

    print("--- Finished test_jewelry_model_str ---")