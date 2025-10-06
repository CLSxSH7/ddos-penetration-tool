# DDoS Penetration Testing Tool

A structured educational tool for authorized DDoS testing in controlled environments.

## ⚠️ LEGAL DISCLAIMER

This tool is for educational purposes and authorized penetration testing only. Unauthorized use of this tool against
systems you do not own or lack explicit written permission to test is illegal and unethical.

## Overview

A multi-threaded HTTP load testing tool designed for legitimate security testing with IP rotation capabilities through
proxy support.

## Features

- Multi-threaded request generation
- User-Agent rotation
- Proxy support for IP address rotation
- Network interface binding
- Real time statistics
- Configurable request parameters

## Installation

### Prerequisites

- Python 3.7+
- pip package manager

### Setup

1. Clone the repository:

```bash
git@github.com:CLSxSH7/ddos-penetration-tool.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Dependencies

- `requests` - HTTP library
- `netifaces` - Network interface detection
- `beautifulsoup4` - HTML parsing (for proxy fetching)
- `urllib3` - HTTP utilities

## Usage

### Basic Usage

```bash
python main.py
```

This will launch the interactive interface where you can:

Enter target URL
Configure thread count
Select attack options
Start the test

## Command Line Options

### Standard Mode

```bash
python main.py
```

Launches the interactive interface

### Free Proxy Mode

```bash
python main.py --use-free-proxies
```

Runs the attack using sample free proxies for IP rotation
Direct execution with target and threads:

```bash
python main.py --use-free-proxies <target_url> <thread_count>
```

Example:

```bash
python main.py --use-free-proxies http://example.com 50
```

### Paid Proxy Mode

```bash
python main.py --use-paid-proxies
```

Runs the attack using paid proxies configured in the code
Direct execution with target and threads:

```bash
python main.py --use-paid-proxies <target_url> <thread_count>
```

Example:

```bash
python main.py --use-paid-proxies http://example.com 50
```

## Configuration

### Adding Paid Proxies

To use paid proxies, edit `ddos_tool/client/ddos_client.py` and add your proxies to the `PAID_PROXIES` list:

```
PAID_PROXIES = [
    "http://username:password@proxy1.example.com:8080",
    "http://username:password@proxy2.example.com:8080",
    "http://proxy3.example.com:8080",  # If no authentication required
]
```

Proxy formats supported:

- HTTP proxies: `http://host:port`
- HTTP proxies with authentication: `http://user:pass@host:port`
- HTTPS proxies: `https://host:port`

### Sample Free Proxies

The tool includes a list of sample free proxies for educational purposes in the `SAMPLE_FREE_PROXIES` section. Note that
these are unreliable and may not work.

## How It Works

### Core Functionality

1. Multi-threading: Uses multiple threads to generate concurrent HTTP requests
2. User-Agent Rotation: Cycles through different browser User-Agent strings
3. IP Address Rotation: Uses proxies to rotate source IP addresses
4. Network Interface Binding: Rotates through available network interfaces

### Proxy Rotation

The tool supports two types of proxy configurations:

1. Sample Free Proxies: Pre-configured list of free public proxies (unreliable)
2. Paid Proxies: Custom list of paid/private proxies (more reliable)

### Network Interface Rotation

Automatically detects available network interfaces and rotates requests through them to distribute load across different
network paths.

## Interface Options

When running in interactive mode, the tool presents several configuration options:

1. Target URL: The HTTP endpoint to test
2. Thread Count: Number of concurrent request threads
3. Attack Options:

- Standard attack (no special features)
- IP rotation with proxies
- Interface binding
- Combined IP rotation and interface binding
- Free proxy rotation (with sample proxies)

## Statistics

The tool tracks and displays real-time statistics:

- Total requests sent
- Successful requests
- Failed requests
- Success rate percentage

Press Ctrl+C to stop the attack at any time and view the final statistics.

## Security Considerations

### Ethical Usage
- Only test systems you own or have explicit written permission to test
- Be aware of potential impact on target systems
- Comply with all applicable laws and regulations
- Respect rate limits and terms of service

### Proxy Security
- Free proxies may log your traffic or inject malicious content
- Paid/private proxies are more secure but still require trust in the provider
- Always use HTTPS endpoints when possible
- Consider the privacy implications of your testing

## Troubleshooting

### Common Issues
1. All proxies failing: Free proxies are often unreliable. Consider using paid proxies for consistent results.

2. "127.0.0.1" in logs: This indicates direct connections when proxies fail. Check proxy configuration and connectivity.

3. SSL errors: The tool disables SSL verification for testing purposes. Ensure you understand the security implications.

4. Permission errors: Run with appropriate permissions for network interface access.

### Debugging
Enable debug output by checking the console logs during execution. The tool shows:
- Proxy selection and usage
- Request successes and failures
- Error details for failed requests