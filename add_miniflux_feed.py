#!/usr/bin/env python3
"""
Script to add an RSS feed to a Miniflux server.

Usage:
    python add_miniflux_feed.py --url FEED_URL --server SERVER_URL --api-key API_KEY
    
    Or set environment variables:
    export MINIFLUX_URL="https://your-miniflux-server.com"
    export MINIFLUX_API_KEY="your-api-key"
    
    python add_miniflux_feed.py --url FEED_URL
"""

import argparse
import os
import sys
import requests
from typing import Optional


def add_feed_to_miniflux(
    feed_url: str,
    server_url: str,
    api_key: str,
    category_id: Optional[int] = None
) -> dict:
    """
    Add a feed to Miniflux server.
    
    Args:
        feed_url: The URL of the RSS/Atom feed to add
        server_url: The Miniflux server URL
        api_key: The Miniflux API key
        category_id: Optional category ID to add the feed to
        
    Returns:
        dict: Response from Miniflux API containing feed details
        
    Raises:
        requests.exceptions.RequestException: If the API request fails
    """
    # Ensure server URL doesn't end with a slash
    server_url = server_url.rstrip('/')
    
    # Prepare the API endpoint
    api_endpoint = f"{server_url}/v1/feeds"
    
    # Prepare headers
    headers = {
        "X-Auth-Token": api_key,
        "Content-Type": "application/json"
    }
    
    # Prepare the payload
    payload = {
        "feed_url": feed_url
    }
    
    if category_id:
        payload["category_id"] = category_id
    
    # Make the API request
    response = requests.post(api_endpoint, json=payload, headers=headers)
    
    # Check if request was successful
    response.raise_for_status()
    
    return response.json()


def main():
    parser = argparse.ArgumentParser(
        description="Add an RSS feed to a Miniflux server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables:
  MINIFLUX_URL      Miniflux server URL (alternative to --server)
  MINIFLUX_API_KEY  Miniflux API key (alternative to --api-key)

Examples:
  %(prog)s --url https://example.com/feed.xml --server https://miniflux.example.com --api-key YOUR_KEY
  
  # Using environment variables
  export MINIFLUX_URL="https://miniflux.example.com"
  export MINIFLUX_API_KEY="YOUR_KEY"
  %(prog)s --url https://example.com/feed.xml
  
  # Add to specific category
  %(prog)s --url https://example.com/feed.xml --category 5
        """
    )
    
    parser.add_argument(
        "--url",
        required=True,
        help="RSS/Atom feed URL to add"
    )
    
    parser.add_argument(
        "--server",
        default=os.environ.get("MINIFLUX_URL"),
        help="Miniflux server URL (or set MINIFLUX_URL env var)"
    )
    
    parser.add_argument(
        "--api-key",
        default=os.environ.get("MINIFLUX_API_KEY"),
        help="Miniflux API key (or set MINIFLUX_API_KEY env var)"
    )
    
    parser.add_argument(
        "--category",
        type=int,
        help="Category ID to add the feed to (optional)"
    )
    
    args = parser.parse_args()
    
    # Validate required parameters
    if not args.server:
        print("Error: Miniflux server URL is required. Use --server or set MINIFLUX_URL environment variable.", 
              file=sys.stderr)
        sys.exit(1)
    
    if not args.api_key:
        print("Error: Miniflux API key is required. Use --api-key or set MINIFLUX_API_KEY environment variable.", 
              file=sys.stderr)
        sys.exit(1)
    
    try:
        print(f"Adding feed: {args.url}")
        print(f"To server: {args.server}")
        
        result = add_feed_to_miniflux(
            feed_url=args.url,
            server_url=args.server,
            api_key=args.api_key,
            category_id=args.category
        )
        
        print("\n✓ Feed added successfully!")
        print(f"Feed ID: {result.get('id')}")
        print(f"Feed Title: {result.get('title', 'N/A')}")
        print(f"Site URL: {result.get('site_url', 'N/A')}")
        
    except requests.exceptions.HTTPError as e:
        print(f"\n✗ HTTP Error: {e}", file=sys.stderr)
        if e.response is not None:
            try:
                error_detail = e.response.json()
                print(f"Error details: {error_detail}", file=sys.stderr)
            except:
                print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)
        
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Request Error: {e}", file=sys.stderr)
        sys.exit(1)
        
    except Exception as e:
        print(f"\n✗ Unexpected Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

