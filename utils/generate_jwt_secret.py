import secrets

def generate_jwt_secret():
    return secrets.token_urlsafe(64)

def update_env_file(jwt_secret):
    # Check if the JWT secret already exists in the .env file
    with open(".env", "r") as env_file:
        existing_lines = env_file.readlines()
        for line in existing_lines:
            if line.strip().startswith("POSTGREST_JWT_SECRET="):
                # JWT secret already exists, no need to update the file
                return

    # JWT secret does not exist, append it to the .env file
    with open(".env", "a") as env_file:
        env_file.write("\nPOSTGREST_JWT_SECRET={}\n".format(jwt_secret))

def main():
    jwt_secret = generate_jwt_secret()
    update_env_file(jwt_secret)
    print("JWT secret key generated and updated in the .env file.")

if __name__ == "__main__":
    main()