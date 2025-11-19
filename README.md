# Miniflux Feed Adder

A simple Python script to add RSS/Atom feeds to a Miniflux server via its API.

## Prerequisites

- Python 3.6 or higher
- A Miniflux server with API access
- A Miniflux API key

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Getting Your API Key

1. Log into your Miniflux server
2. Go to Settings → API Keys
3. Create a new API key or copy an existing one

## Usage

### Basic Usage

```bash
python add_miniflux_feed.py --url FEED_URL --server SERVER_URL --api-key API_KEY
```

### Using Environment Variables

Set your Miniflux credentials as environment variables:

```bash
export MINIFLUX_URL="https://your-miniflux-server.com"
export MINIFLUX_API_KEY="your-api-key-here"
```

Then simply run:

```bash
python add_miniflux_feed.py --url https://example.com/feed.xml
```

### List Available Categories

```bash
python add_miniflux_feed.py --list-categories
```

### Add to Specific Category

```bash
python add_miniflux_feed.py --url https://example.com/feed.xml --category "Technology"
```

## Examples

```bash
# Add a feed with explicit credentials
python add_miniflux_feed.py \
  --url https://hnrss.org/newest \
  --server https://miniflux.example.com \
  --api-key your-api-key-123

# Add a feed using environment variables
export MINIFLUX_URL="https://miniflux.example.com"
export MINIFLUX_API_KEY="your-api-key-123"
python add_miniflux_feed.py --url https://hnrss.org/newest

# Add to category by name
python add_miniflux_feed.py --url https://example.com/rss --category "News"

# List all available categories
python add_miniflux_feed.py --list-categories
```

## Options

- `--url`: The RSS/Atom feed URL to add (required when adding a feed)
- `--server`: Miniflux server URL (or use `MINIFLUX_URL` environment variable)
- `--api-key`: Miniflux API key (or use `MINIFLUX_API_KEY` environment variable)
- `--category`: Optional category name to add the feed to (case-insensitive)
- `--list-categories`: List all available categories and exit

## Error Handling

The script will:
- Validate that server URL and API key are provided
- Display clear error messages if the feed cannot be added
- If an invalid category name is provided, show all available categories
- Show the feed details upon successful addition

## Miniflux API Documentation

For more information about the Miniflux API, visit:
https://miniflux.app/docs/api.html

