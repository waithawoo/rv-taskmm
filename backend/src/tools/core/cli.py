import os
import sys

from utils import generate_app_key, generate_env_file, get_common_jwt_algorithms

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# SRC_DIR = os.path.join(BASE_DIR, 'src', 'modules')
# TEMPLATE_DIR = os.path.join(BASE_DIR, 'module_templates')

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# SRC_DIR = os.path.join(BASE_DIR, 'src', 'modules')
# TEMPLATE_DIR = os.path.join(BASE_DIR, 'tools', 'module_templates')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  
SRC_DIR = os.path.join(BASE_DIR, 'modules')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'tools/core', 'module_templates')

# print('Base Directory:', BASE_DIR)
# print('Source Directory:', SRC_DIR)
# print('Template Directory:', TEMPLATE_DIR)

# exit()

TEMPLATE_FILES = {
    '__init__.py': os.path.join(TEMPLATE_DIR, '__init__.py'),
    'constants.py': os.path.join(TEMPLATE_DIR, 'constants.py'),
    'dependencies.py': os.path.join(TEMPLATE_DIR, 'dependencies.py'),
    'exceptions.py': os.path.join(TEMPLATE_DIR, 'exceptions.py'),
    'models.py': os.path.join(TEMPLATE_DIR, 'models.py'),
    'repositories.py': os.path.join(TEMPLATE_DIR, 'repositories.py'),
    'routes.py': os.path.join(TEMPLATE_DIR, 'routes.py'),
    'schemas.py': os.path.join(TEMPLATE_DIR, 'schemas.py'),
    'services.py': os.path.join(TEMPLATE_DIR, 'services.py'),
    'utils.py': os.path.join(TEMPLATE_DIR, 'utils.py'),
}

def convert_to_pascal_case(s: str) -> str:
    # Split the string by underscores, capitalize each part, and join them together
    return ''.join(word.capitalize() for word in s.split('_'))

def create_module(module_name):
    """Create a module with the given name."""
    module_path = os.path.join(SRC_DIR, module_name)
    if os.path.exists(module_path):
        print('module dir already existed. Skipped')
        exit()
        
    os.makedirs(module_path, exist_ok=True)
    
    print(f'Creating module: {module_name}')
    
    for file_name, template_path in TEMPLATE_FILES.items():
        output_file = os.path.join(module_path, file_name)
        with open(template_path, 'r') as template_file:
            template_content = template_file.read()
        
        # Replace placeholders
        content = template_content.replace('{module_name}', module_name).replace(
            '{ModelName}', convert_to_pascal_case(module_name)
        )
        
        # Write the new content
        with open(output_file, 'w') as output:
            output.write(content)
        print(f'Created {output_file}')

def generate_app_secret_key(length=64):
    print(generate_app_key(length))

def generate_env_command(algorithm='HS256'):
    """Generate .env file with JWT values filled."""
    try:
        generate_env_file(algorithm=algorithm)
    except Exception as e:
        print(f"Error generating .env file: {e}")
        sys.exit(1)

def show_jwt_algorithms():
    """Show available JWT algorithms."""
    algorithms = get_common_jwt_algorithms()
    print("Available JWT algorithms:")
    for i, alg in enumerate(algorithms, 1):
        print(f"  {i}. {alg}")
    
def main():

    if len(sys.argv) < 2:
        print('Usage: python cli.py <command>:<action> [param]')
        print('Commands:')
        print('  create:module <module_name>     - Create a new module')
        print('  generate:key <length>           - Generate app secret key')
        print('  generate:env [algorithm]        - Generate .env file with JWT values')
        print('  show:algorithms                 - Show available JWT algorithms')
        print('')
        print('Examples:')
        print('  python cli.py create:module user_profile')
        print('  python cli.py generate:key 64')
        print('  python cli.py generate:env HS256')
        print('  python cli.py show:algorithms')
        return

    command_action = sys.argv[1]
    param = sys.argv[2] if len(sys.argv) > 2 else None

    if ':' not in command_action:
        print('Invalid command format. Use <command>:<action>')
        return

    command, action = command_action.split(':')

    if command == 'create':
        if action == 'module':
            if not param:
                print('Module name is required')
                return
            create_module(str(param))
        else:
            print(f'Unknown create action: {action}')
    elif command == 'generate':
        if action == 'key':
            length = int(param) if param else 64
            generate_app_secret_key(length)
        elif action == 'env':
            algorithm = param if param else 'HS256'
            generate_env_command(algorithm)
        else:
            print(f'Unknown generate action: {action}')
    elif command == 'show':
        if action == 'algorithms':
            show_jwt_algorithms()
        else:
            print(f'Unknown show action: {action}')
    else:
        print('Invalid command.')

if __name__ == '__main__':
    main()
