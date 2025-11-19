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


def get_categories(server_url: str, api_key: str) -> list:
    """
    Get all categories from Miniflux server.
    
    Args:
        server_url: The Miniflux server URL
        api_key: The Miniflux API key
        
    Returns:
        list: List of category dictionaries with 'id' and 'title' fields
        
    Raises:
        requests.exceptions.RequestException: If the API request fails
    """
    # Ensure server URL doesn't end with a slash
    server_url = server_url.rstrip('/')
    
    # Prepare the API endpoint
    api_endpoint = f"{server_url}/v1/categories"
    
    # Prepare headers
    headers = {
        "X-Auth-Token": api_key,
        "Content-Type": "application/json"
    }
    
    # Make the API request
    response = requests.get(api_endpoint, headers=headers)
    
    # Check if request was successful
    response.raise_for_status()
    
    return response.json()


def get_category_id_by_name(server_url: str, api_key: str, category_name: str) -> int:
    """
    Get category ID by category name.
    
    Args:
        server_url: The Miniflux server URL
        api_key: The Miniflux API key
        category_name: The name of the category
        
    Returns:
        int: The category ID
        
    Raises:
        ValueError: If category not found
        requests.exceptions.RequestException: If the API request fails
    """
    categories = get_categories(server_url, api_key)
    
    # Search for category by name (case-insensitive)
    for category in categories:
        if category['title'].lower() == category_name.lower():
            return category['id']
    
    # If not found, raise an error with available categories
    available = ", ".join([f"'{cat['title']}'" for cat in categories])
    raise ValueError(f"Category '{category_name}' not found. Available categories: {available}")


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
  # Add a feed with explicit credentials
  %(prog)s --url https://example.com/feed.xml --server https://miniflux.example.com --api-key YOUR_KEY
  
  # Using environment variables
  export MINIFLUX_URL="https://miniflux.example.com"
  export MINIFLUX_API_KEY="YOUR_KEY"
  %(prog)s --url https://example.com/feed.xml
  
  # Add to specific category by name
  %(prog)s --url https://example.com/feed.xml --category "Technology"
  
  # List all available categories
  %(prog)s --list-categories
        """
    )
    
    parser.add_argument(
        "--url",
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
        type=str,
        help="Category name to add the feed to (optional)"
    )
    
    parser.add_argument(
        "--list-categories",
        action="store_true",
        help="List all available categories and exit"
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
    
    # Handle list-categories command
    if args.list_categories:
        try:
            print(f"Fetching categories from: {args.server}\n")
            categories = get_categories(args.server, args.api_key)
            
            if not categories:
                print("No categories found.")
            else:
                print(f"Available categories ({len(categories)}):\n")
                for category in categories:
                    print(f"  • {category['title']} (ID: {category['id']})")
            
            sys.exit(0)
            
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
    
    # Validate URL is required when not listing categories
    if not args.url:
        print("Error: --url is required when adding a feed. Use --help for usage information.", 
              file=sys.stderr)
        sys.exit(1)
    
    try:
        print(f"Adding feed: {args.url}")
        print(f"To server: {args.server}")
        
        # Look up category ID by name if category is specified
        category_id = None
        if args.category:
            print(f"Looking up category: {args.category}")
            category_id = get_category_id_by_name(
                server_url=args.server,
                api_key=args.api_key,
                category_name=args.category
            )
            print(f"Found category ID: {category_id}")
        
        result = add_feed_to_miniflux(
            feed_url=args.url,
            server_url=args.server,
            api_key=args.api_key,
            category_id=category_id
        )
        
        print("\n✓ Feed added successfully!")
        print(f"Feed ID: {result.get('id')}")
        print(f"Feed Title: {result.get('title', 'N/A')}")
        print(f"Site URL: {result.get('site_url', 'N/A')}")
        
    except ValueError as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)
        
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

