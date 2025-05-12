import hashlib
import secrets


def hash_password(password):
    """
    Hash a password using SHA-256.
    :param password: The password to hash.
    :return: The hashed password.
    """
    return hashlib.sha256(password.encode()).hexdigest()

# USER: PW-Hash
users = {}
with open("users.csv"):
    for line in open("users.csv"):
        username, password = line.strip().split(",")
        users[username] = password
        print(hash_password(password))



def check_request(request):
    """
    Check if the request is valid and implement a token system.
    :param request: The request to check.
    :return: A token if the request is valid, None otherwise.
    """

    # Check if the request is valid
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)
        if username in users and users[username] == hashed_password:
            # Generate a token for the user
            token = secrets.token_hex(16)
            # Store the token (in a real application, use a secure storage)
            users[username] = {'password': hashed_password, 'token': token}
            return token
    # get the cookie from the request token
    # check if the token is valid
    if 'token' in request.cookies:
        token = request.cookies.get('token')
        for user, data in users.items():
            try:
                if data.get('token') == token:
                    return token 
            except:
                # Handle the case where data is not a dictionary
                continue  
    return None