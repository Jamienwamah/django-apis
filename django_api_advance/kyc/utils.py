import requests
from .models import KYCVerification
from django.conf import settings

def verify_kyc(user_id):
    """
    Function to verify KYC using Watu API and record the verification status in Django models
    :param user_id: User ID for KYC verification
    :return: Verification result (True or False)
    """
    api_key = settings# .CLIENT_KEY  # Replace with your actual API key
    watu_api_url = f'api url_link"{api_key}&user_id={user_id}'

    try:
        response = requests.post(watu_api_url)
        if response.status_code == 200:
            # Process the response from Watu API
            verification_result = response.json().get('verified', False)
            
            # Update the KYCVerification model
            kyc_verification, _ = KYCVerification.objects.get_or_create(user_id=user_id)
            kyc_verification.verified = verification_result
            kyc_verification.save()
            
            return verification_result
        else:
            # Handle error response from Watu API
            return None
    except requests.exceptions.RequestException as e:
        # Handle connection errors
        print(f"Error connecting to Watu API: {e}")
        return None
