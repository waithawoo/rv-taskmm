import base64
import json
from typing import Any, Dict
from datetime import datetime
from decimal import Decimal


def build_db_url( 
    db_username: str,
    db_password: str,
    db_host: str,
    db_port: int,
    db_name: str,) -> str:
    from urllib.parse import quote_plus
    return (
        f'mysql+asyncmy://{quote_plus(db_username)}:{quote_plus(db_password)}'
        f'@{db_host}:{db_port}/{db_name}'
    )


def destruct_db_url(db_url: str) -> Dict[str, str | int]:
    from urllib.parse import urlparse, unquote_plus

    parsed = urlparse(db_url)

    return {
        'db_username': unquote_plus(parsed.username) if parsed.username else '',
        'db_password': unquote_plus(parsed.password) if parsed.password else '',
        'db_host': parsed.hostname or '',
        'db_port': parsed.port or 3306,
        'db_name': parsed.path.lstrip('/'),
    }


def encode_cursor(cursor_data: Dict[str, Any]) -> str:
    if cursor_data is None:
        return None
    
    def json_serializer(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    try:
        json_str = json.dumps(cursor_data, default=json_serializer)
        return base64.b64encode(json_str.encode()).decode()
    except Exception as e:
        raise


def decode_cursor(cursor_token: str) -> Dict[str, Any]:
    if not cursor_token:
        return None
    
    try:
        json_str = base64.b64decode(cursor_token.encode()).decode()
        cursor_data = json.loads(json_str)
        
        if isinstance(cursor_data, dict):
            for key, value in cursor_data.items():
                if isinstance(value, str) and 'T' in value:
                    try:
                        cursor_data[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except ValueError:
                        pass
        
        return cursor_data
    except Exception as e:
        return None
