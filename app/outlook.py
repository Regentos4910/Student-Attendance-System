import msal
from flask import current_app

def get_outlook_token():
    client_id = current_app.config['MS_CLIENT_ID']
    authority = f"https://login.microsoftonline.com/{current_app.config['MS_TENANT_ID']}"
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=current_app.config['MS_CLIENT_SECRET']
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return result['access_token']

def send_outlook_email(parent_email, subject, body):
    import requests
    token = get_outlook_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    email_data = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": body
            },
            "toRecipients": [{
                "emailAddress": {
                    "address": parent_email
                }
            }]
        }
    }
    response = requests.post(
        "https://graph.microsoft.com/v1.0/me/sendMail",
        headers=headers,
        json={"message": email_data}
    )
    return response.status_code == 202
