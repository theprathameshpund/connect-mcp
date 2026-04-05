# Loan MCP Plugin

## Overview

This plugin enables Claude to interact with a loan system using MCP tools.

---

## Capabilities

- Create Loan
- Approve Loan
- Delete Loan


---

## Available Tools
- **create_loan**: Create a loan for a borrower
- **approve_loan**: Approve a loan for a borrower
- **delete_loan**: Delete a loan for a borrower


---

## Architecture

Claude (CoWork)
        |
        v
Claude Plugin
        |
        v
MCP Server (SSE)
        |
        v
Backend System

---

## How It Works

- Claude reads skills from the `skills/` directory
- Each skill maps to an MCP tool
- The MCP server executes tool calls
- Results are returned to Claude

---

## Notes

- MCP server must be running and accessible
- Uses SSE transport
- Plugin generated automatically from MCP server

---

## Author

Your Name
