#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from utils import generate_env_file, get_common_jwt_algorithms


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print("Usage: python generate_env.py [algorithm]")
        print("")
        print("Generate .env file from .env.example with JWT values filled.")
        print("")
        print("Arguments:")
        print("  algorithm    JWT algorithm to use (default: HS256)")
        print("")
        print("Available algorithms:")
        algorithms = get_common_jwt_algorithms()
        for alg in algorithms:
            print(f"  - {alg}")
        print("")
        print("Examples:")
        print("  python generate_env.py")
        print("  python generate_env.py HS256")
        print("  python generate_env.py RS256")
        return

    algorithm = sys.argv[1] if len(sys.argv) > 1 else 'HS256'
    
    valid_algorithms = get_common_jwt_algorithms()
    if algorithm not in valid_algorithms:
        print(f"Invalid algorithm: {algorithm}")
        print(f"Available algorithms: {', '.join(valid_algorithms)}")
        sys.exit(1)
    
    try:
        generate_env_file(algorithm=algorithm)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
