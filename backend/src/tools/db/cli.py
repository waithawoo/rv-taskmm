import os
import datetime

MIGRATIONS_PATH = 'migrations'

def create_migration(name):
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f'{timestamp}_{name}.sql'
    filepath = os.path.join(MIGRATIONS_PATH, filename)
    with open(filepath, 'w') as file:
        file.write('-- up\n\n-- down\n')
    print(f'Created migration: {filepath}')

def apply_migrations():
    os.system('python src/tools/db/migration_tool.py')

def seed_data():
    os.system('python src/tools/db/seed.py')
    
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: cli.py <command> [args] <options.')
        sys.exit(1)
    
    print('sys last ', sys.argv[-1])
    command = sys.argv[1]
    options =  sys.argv[-1] if sys.argv[-1].startswith('--') else ''
    
    if command == 'create':
        if len(sys.argv) < 3:
            print('Usage: cli.py create <migration_name1>, <migration_name2> --refresh')
            sys.exit(1)
        for each in sys.argv[2:]:
            create_migration(each)
    elif command == 'migrate':
        apply_migrations()
    elif command == 'seed':
        seed_data()
    else:
        print('Unknown command')
