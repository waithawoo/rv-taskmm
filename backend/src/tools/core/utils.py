import secrets
import os
import shutil


def generate_app_key(length=64):
    return secrets.token_hex(length // 2)


def generate_jwt_secret(length=64):
    return secrets.token_urlsafe(length)


def get_common_jwt_algorithms():
    return ['HS256', 'HS384', 'HS512', 'RS256', 'RS384', 'RS512']


def generate_env_file(source_path=None, target_path=None, algorithm='HS256'):
    """
    Generate .env file from .env.example with JWT values filled.
    
    Args:
        source_path: Path to .env.example file (defaults to src/.env.example)
        target_path: Path where .env should be created (defaults to src/.env)
        algorithm: JWT algorithm to use (default: HS256)
    """
    # Set default paths
    if source_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        source_path = os.path.join(base_dir, '.env.example')
    
    if target_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        target_path = os.path.join(base_dir, '.env')
    
    # Check if source file exists
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source file not found: {source_path}")
    
    # Check if target file already exists
    if os.path.exists(target_path):
        response = input(f"File {target_path} already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            return
    
    # Generate JWT values
    jwt_secret = generate_jwt_secret()
    jwt_algorithm = algorithm
    
    # Read the template file and replace JWT values
    with open(source_path, 'r') as f:
        content = f.read()
    
    # Replace empty JWT values
    content = content.replace('JWT_SECRET=', f'JWT_SECRET={jwt_secret}')
    content = content.replace('JWT_ALGORITHM=', f'JWT_ALGORITHM={jwt_algorithm}')
    
    # Write the new .env file
    with open(target_path, 'w') as f:
        f.write(content)
    
    print(f".env file generated successfully at: {target_path}")
    print(f"JWT_SECRET: {jwt_secret[:20]}...")
    print(f"JWT_ALGORITHM: {jwt_algorithm}")
    print("\nRemember to:")
    print("   - Set your database credentials")
    print("   - Set your Redis URL if using Redis")
