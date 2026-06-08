"""
Ghost CMS Automation Bridge.

This module provides functions to interact with the Ghost Admin API to create
and publish posts. It is designed to be used by the Content Writer agent to
automatically publish articles when anomalies are detected.
"""

import os
import json
import time
import logging
from typing import List, Optional, Dict, Any

import jwt
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(override=True)

GHOST_ADMIN_API_KEY = os.getenv("GHOST_ADMIN_API_KEY")
GHOST_API_URL = "https://www.open-reporting.dev/ghost/api/admin/"


class GhostAPIError(Exception):
    """Custom exception for Ghost API errors."""
    pass


def _get_jwt() -> str:
    """
    Generate a JWT token for Ghost Admin API authentication.
    """
    if not GHOST_ADMIN_API_KEY:
        raise ValueError("GHOST_ADMIN_API_KEY environment variable is not set.")

    try:
        # Split the key into ID and SECRET
        id_part, secret_part = GHOST_ADMIN_API_KEY.split(':')
    except ValueError:
        raise ValueError("GHOST_ADMIN_API_KEY must be in the format 'id:secret'")

    # Prepare header and payload
    iat = int(time.time())
    header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id_part}
    payload = {
        'iat': iat,
        'exp': iat + 5 * 60,
        'aud': '/admin/'
    }

    # Create the token (including decoding secret)
    # Ghost secret is hex encoded, so we need to decode it to bytes
    secret_bytes = bytes.fromhex(secret_part)
    token = jwt.encode(payload, secret_bytes, algorithm='HS256', headers=header)
    
    # In PyJWT < 2.0, encode returns bytes. In 2.0+, it returns str.
    if isinstance(token, bytes):
        token = token.decode('utf-8')
        
    return token


def _make_request(method: str, endpoint: str, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Make an authenticated request to the Ghost Admin API.
    """
    token = _get_jwt()
    headers = {
        'Authorization': f'Ghost {token}',
        'Content-Type': 'application/json',
    }

    url = f"{GHOST_API_URL.rstrip('/')}/{endpoint.lstrip('/')}"
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, json=json_data)
        elif method.upper() == 'PUT':
            response = requests.put(url, headers=headers, json=json_data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP Error {e.response.status_code}: {e.response.text}"
        logger.error(error_msg)
        raise GhostAPIError(error_msg) from e
    except requests.exceptions.RequestException as e:
        logger.error(f"Request Error: {str(e)}")
        raise GhostAPIError(f"Failed to communicate with Ghost API: {str(e)}") from e


def create_draft_post(title: str, markdown_content: str, tags: Optional[List[str]] = None) -> str:
    """
    Create a new draft post in Ghost with the provided markdown content.
    
    Args:
        title (str): The title of the post.
        markdown_content (str): The markdown content of the post.
        tags (List[str], optional): A list of tags to apply to the post.
        
    Returns:
        str: The ID of the created post.
    """
    # Create mobiledoc with a markdown card
    mobiledoc = {
        "version": "0.3.1",
        "markups": [],
        "atoms": [],
        "cards": [
            [
                "markdown",
                {
                    "cardName": "markdown",
                    "markdown": markdown_content
                }
            ]
        ],
        "sections": [
            [10, 0]
        ]
    }
    
    post_data = {
        "title": title,
        "mobiledoc": json.dumps(mobiledoc),
        "status": "draft"
    }
    
    if tags:
        # Ghost accepts tags as an array of objects
        post_data["tags"] = [{"name": tag} for tag in tags]
        
    payload = {
        "posts": [post_data]
    }
    
    logger.info(f"Creating draft post: '{title}'")
    response = _make_request('POST', 'posts/', json_data=payload)
    
    if 'posts' not in response or not response['posts']:
        raise GhostAPIError("Invalid response from Ghost API: no posts returned")
        
    post_id = response['posts'][0]['id']
    logger.info(f"Successfully created draft post with ID: {post_id}")
    return post_id


def publish_post(post_id: str) -> bool:
    """
    Publish an existing draft post.
    
    Args:
        post_id (str): The ID of the post to publish.
        
    Returns:
        bool: True if successfully published.
    """
    # To update a post, Ghost requires its updated_at field, so we must fetch it first.
    logger.info(f"Fetching post details for ID: {post_id}")
    get_response = _make_request('GET', f'posts/{post_id}/')
    
    if 'posts' not in get_response or not get_response['posts']:
        raise GhostAPIError(f"Post with ID {post_id} not found")
        
    post = get_response['posts'][0]
    updated_at = post['updated_at']
    
    update_data = {
        "posts": [
            {
                "status": "published",
                "updated_at": updated_at
            }
        ]
    }
    
    logger.info(f"Publishing post ID: {post_id}")
    response = _make_request('PUT', f'posts/{post_id}/', json_data=update_data)
    
    if 'posts' in response and response['posts'][0]['status'] == 'published':
        logger.info(f"Successfully published post ID: {post_id}")
        return True
        
    raise GhostAPIError(f"Failed to publish post. Response: {json.dumps(response)}")
