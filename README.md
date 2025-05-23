# GitHub MCP Server

A Model Context Protocol (MCP) server that provides GitHub integration tools for AI assistants. This server implements a set of tools that allow AI models to interact with GitHub repositories, issues, pull requests, and content.

## Features

- Repository Management
  - List repositories
  - Get repository details
- Issue Management
  - List issues
  - Create issues
- Pull Request Management
  - List pull requests
  - Create pull requests
- Content Management
  - Get file content
  - List directory contents

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/github-mcp.git
cd github-mcp
```

2. Install the package:

```bash
pip install -e .
```

## Authentication

This server uses `githubauthlib` for secure GitHub authentication. The library retrieves GitHub tokens from your system's keychain:

- macOS: Uses Keychain Access
- Windows: Uses Credential Manager
- Linux: Uses libsecret

To set up authentication:

1. Install the required system dependencies:

   - macOS: No additional setup required
   - Windows: No additional setup required
   - Linux: Install libsecret

     ```bash
     # Ubuntu/Debian
     sudo apt-get install libsecret-tools

     # Fedora
     sudo dnf install libsecret
     ```

2. Configure your GitHub credentials:
   - The server will automatically use your Git credentials from the system keychain
   - If no credentials are found, you'll need to configure Git with your GitHub credentials:

     ```bash
     git config --global credential.helper store
     # Then perform a Git operation that requires authentication
     ```

## Usage

1. Start the server:

```bash
python -m github_mcp.server
```

The server will start on `http://localhost:8000` by default.

2. Configure Cursor IDE:
   - Open Cursor IDE settings
   - Add the following MCP server configuration:

     ```json
     {
       "mcp": {
         "servers": [
           {
             "name": "github-mcp",
             "url": "http://localhost:8000/sse"
           }
         ]
       }
     }
     ```

## API Endpoints

- `GET /`: Server information and available tools
- `POST /tool`: Synchronous tool calls
- `GET /sse`: Server-Sent Events endpoint for streaming responses

## Available Tools

### Repository Tools

- `list_repositories`: List GitHub repositories
  - Parameters:
    - `visibility` (optional): "all", "public", or "private"
    - `sort` (optional): "created", "updated", "pushed", or "full_name"
- `get_repository`: Get repository details
  - Parameters:
    - `owner`: Repository owner
    - `repo`: Repository name

### Issue Tools

- `list_issues`: List repository issues
  - Parameters:
    - `owner`: Repository owner
    - `repo`: Repository name
    - `state` (optional): "open", "closed", or "all"
    - `labels` (optional): List of label names
- `create_issue`: Create a new issue
  - Parameters:
    - `owner`: Repository owner
    - `repo`: Repository name
    - `title`: Issue title
    - `body` (optional): Issue description
    - `labels` (optional): List of label names
    - `assignees` (optional): List of assignee usernames

### Pull Request Tools

- `list_pull_requests`: List repository pull requests
  - Parameters:
    - `owner`: Repository owner
    - `repo`: Repository name
    - `state` (optional): "open", "closed", or "all"
    - `sort` (optional): "created", "updated", "popularity", or "long-running"
- `create_pull_request`: Create a new pull request
  - Parameters:
    - `owner`: Repository owner
    - `repo`: Repository name
    - `title`: Pull request title
    - `body` (optional): Pull request description
    - `head`: Source branch
    - `base` (optional): Target branch (default: "main")
    - `draft` (optional): Create as draft (default: false)

### Content Tools

- `get_file_content`: Get file content
  - Parameters:
    - `owner`: Repository owner
    - `repo`: Repository name
    - `path`: File path
    - `ref` (optional): Branch/tag/commit reference
- `list_directory`: List directory contents
  - Parameters:
    - `owner`: Repository owner
    - `repo`: Repository name
    - `path` (optional): Directory path (default: "")
    - `ref` (optional): Branch/tag/commit reference

## Development

1. Install development dependencies:

```bash
pip install -e ".[dev]"
```

2. Run tests:

```bash
pytest
```

3. Run linting:

```bash
ruff check .
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io)
- [Cursor IDE](https://cursor.com)
- [GitHub API](https://docs.github.com/en/rest)
