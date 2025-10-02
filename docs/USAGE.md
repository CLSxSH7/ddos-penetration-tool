# Usage Guide

## Prerequisites

- Python 3.7 or higher
- pip package manager

## Installation

**1. Clone the repository:**

```bash
git clone git@github.com:CLSxSH7/ddos-penetration-tool.git
cd ddos-penetration-tool
```

**2. Install dependencies:**

```bash
pip install -r requirements.txt
```

## Running the Tool

### Basic Usage

`cd src/ddos_tool/main.py`

```bash
python main.py
```

## Menu Navigation

**1. Main Menu:**
    - Option 1: Configure and start attack
    - Option 2: Exit

**2. Attack Configuration:**
    - Option 1: Start attack with current settings
    - Option 2: Change target
    - Option 3: Change thread count
    - Option 4: Return to main menu

## Supported Target Formats

- Full URLs: `http://example.com`, `https://test.org`
- Domains: `example.com`, `test.org`
- IP addresses: `192.168.1.1`, `10.0.0.1`

## Thread Configuration

- Minimum threads: 1
- Maximum threads: 1000
- Default: 50 threads

## Stopping an Attack

Press `Ctrl+C` at any time to gracefully stop the attack. The tool will display a summary of requests sent.

## Safety Guidelines

1. Only test systems you own or have explicit written permission to test
2. Monitor system resources during testing
3. Start with low thread counts and increase gradually
4. Document all testing activities
5. Ensure network compliance with your organization's policies
