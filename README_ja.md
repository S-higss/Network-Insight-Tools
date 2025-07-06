# Network-Insight-Tools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

`Network-Insight-Tools` is a collection of Python scripts designed for basic network analysis and information gathering. It aims to help users understand fundamental network behaviors, troubleshoot issues, and learn about security concepts by discovering services through port scanning and investigating domain registration and DNS information.

## Purpose

This repository was developed with the following objectives:

1.  **Network Visibility**: Identify publicly exposed services on a target host through TCP port scanning.
2.  **Domain Information Gathering**: Collect WHOIS registration details and DNS records (IP addresses, MX records, NS records, etc.) for a given domain.
3.  **Learning and Research**: Provide practical examples to understand network mechanisms, fundamental protocols (TCP/IP, DNS, WHOIS), and security countermeasures (ASLR, SSP, etc.).
4.  **Development Environment**: Offer a sample server like `tcp_server.py` to facilitate testing and verification of client tools like `tcp_port_scanner.py`.

## Features

* **TCP Port Scanner (`tcp_port_scanner.py`)**:
    * Scans a specified range of TCP ports on a target host to determine if ports are `OPEN` or `CLOSED`.
    * Utilizes `concurrent.futures.ThreadPoolExecutor` for concurrent processing, enabling fast scans.
    * Displays data received from open ports (e.g., welcome messages from servers).
* **Domain Information Tool (`domain_info.py`)**:
    * Executes WHOIS queries for user-input domain names to retrieve registration details (registrar, creation date, expiration date, name servers, etc.).
    * Performs NSLOOKUP (DNS queries) to obtain IP addresses (IPv4/IPv6), Mail Exchange (MX) records, and Name Server (NS) records associated with the domain.
* **TCP Sample Server (`tcp_server.py`)**:
    * A simple multi-threaded server that listens on multiple predefined TCP ports.
    * Can be used as a sample for verifying the behavior of `tcp_port_scanner.py` and for investigating basic TCP communication.

## File Structure

```
├── network_insight_tools
|   ├── tcp_server.py
|   ├── tcp_port_scanner.py
|   └── domain_info.py
├── README_ja.md
└── README.md
```

## Setup

### Prerequisites

* Python 3.6+ installed.
* `pip` package manager available.

### Installing Required Libraries

Run the following command to install the necessary Python libraries:

```bash
pip install python-whois dnspython
```

## How to Use Each Tool

### 1. TCP Sample Server (`tcp_server.py`)

This is an auxiliary tool for testing `tcp_port_scanner.py`.

1.  **Start the Server:**
    Open a new terminal and run the following command:
    ```bash
    python3 tcp_server.py
    ```
    The server will start listening on `127.0.0.1` (localhost) on ports `8000, 8001, 8002, 8080`.

    *Server Output Example:*
    ```
    Starting TCP/IP Server...
    Server listening on 127.0.0.1:8000...
    Server listening on 127.0.0.1:8001...
    ...
    All server threads started. Listening on ports: [8000, 8001, 8002, 8080]
    Press Ctrl+C to stop the server.
    ```
2.  To stop the server, press `Ctrl+C` in the terminal.

### 2. TCP Port Scanner (`tcp_port_scanner.py`)

1.  **Start the Client:**
    While the server is running, open another terminal and execute the following command:
    ```bash
    python3 tcp_port_scanner.py
    ```

    *Client Output Example:*
    ```
    Starting TCP Port Scan on 127.0.0.1 from port 7999 to 8081...

    --- Scan Results ---
    Target: 127.0.0.1
    Scanned Ports: 7999-8081

    Open Ports:
      8000: OPEN (Service: Hello from TCP server on port 8000!)
      8001: OPEN (Service: Hello from TCP server on port 8001!)
      8002: OPEN (Service: Hello from TCP server on port 8002!)
      8080: OPEN (Service: Hello from TCP server on port 8080!)

    Closed/Filtered Ports:
      7999: CLOSED (Connection refused)
      8003: CLOSED (Connection refused)
      ... (many closed ports) ...

    Scan complete.
    ```
    *The server's terminal will display connection logs during the scan.*

### 3. Domain Information Tool (`domain_info.py`)

1.  **Start the Tool:**
    Run the following command in any terminal:
    ```bash
    python3 domain_info.py
    ```
2.  **Enter a Domain Name:**
    When prompted, type the domain name you wish to investigate (e.g., `google.com`, `example.org`) and press Enter.
    *Type `exit` to quit.*

    *Tool Output Example:*
    ```
    --- Domain Information Tool (WHOIS & NSLOOKUP) ---
    This tool fetches registration details and IP addresses for a given domain.

    Enter a domain name (e.g., example.com) or 'exit' to quit: example.com

    Processing domain: example.com

    --- WHOIS Information for example.com ---
    Domain Name: EXAMPLE.COM
    Registrar: IANA
    WHOIS Server: whois.iana.org
    ... (WHOIS registration information) ...

    --- NSLOOKUP (DNS Information) for example.com ---
    IPv4 Addresses (A records):
      93.184.216.34

    IPv6 Addresses (AAAA records):
      2606:2800:220:1:248:1893:25c8:1946

    Mail Exchange (MX) Records:
      No MX records found.

    Name Server (NS) Records:
      a.iana-servers.net.
      b.iana-servers.net.

    ============================================================
    Enter a domain name (e.g., example.com) or 'exit' to quit: exit
    Exiting tool. Goodbye!
    ```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details. (If a `LICENSE` file is to be created separately, keep this line. Otherwise, it can be removed.)
