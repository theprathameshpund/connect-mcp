# Loan MCP Plugin

## Overview

This plugin enables Claude to interact with a loan system using MCP tools.

---

## Capabilities

- Create Loan
- Get Loan
- Approve Loan


---

## Available Tools
- **create_loan**: Create a new loan for a borrower with a specified amount
- **get_loan**: Fetch loan details using the loan ID
- **approve_loan**: Approve an existing loan by loan ID


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
