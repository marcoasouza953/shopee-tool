# Agent Instance

This project follows the 3-layer agent architecture described in [AGENTE.md](AGENTE.md).

## Structure

- **directives/**: Standard Operating Procedures (SOPs) in Markdown. (Layer 1)
- **execution/**: Deterministic Python scripts. (Layer 3)
- **.tmp/**: Temporary intermediate files. (Never committed)

## Setup

1. Copy `.env.example` to `.env` and fill in your credentials.
2. Put your Google OAuth credentials in `credentials.json` if needed.
