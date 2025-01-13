import random
import string

def generate_password(length=12):
    """Generate a medium-strength password with a mix of characters."""
    if length < 8:
        raise ValueError("Password length should be at least 8 characters for medium strength.")

    # Define character pools
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_characters = "!@#$%^&*()_+-=[]{}|;:,.<>?/"

    # Ensure the password includes at least one character from each pool
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(special_characters)
    ]

    # Fill the rest of the password length with a random mix of all character pools
    all_characters = lowercase + uppercase + digits + special_characters
    password += random.choices(all_characters, k=length - 4)

    # Shuffle the password to ensure randomness
    random.shuffle(password)

    return ''.join(password)

if __name__ == "__main__":
    print("Welcome to the Medium Password Generator!")
    try:
        length = int(input("Enter the desired password length (minimum 8): "))
        password = generate_password(length)
        print(f"Generated Password: {password}")
    except ValueError as e:
        print(f"Error: {e}")
