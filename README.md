# Network Traffic Analyzer

A powerful GUI-based network traffic analysis tool that helps you monitor, analyze, and investigate network traffic in real-time. Perfect for network administrators, security researchers, and developers who need to debug network-related issues.

## Features

- Real-time packet capture and analysis
- Protocol breakdown statistics
- Network forensics capabilities
- Process-to-connection mapping
- Support for common protocols (TCP, UDP, DNS, ICMP, etc.)
- Auto-scrolling packet view
- Detailed protocol analysis

## Prerequisites

- Python 3.8 or higher
- Administrator privileges (required for packet capture)
- Windows OS (tested on Windows 10/11)

## Installation

1. Clone or download this repository to your local machine.

2. Install the required Python packages:
```bash
pip install tkinter
pip install scapy
pip install pandas
pip install psutil
```

3. If you're on Windows, you'll need Npcap for packet capture:
   - Download Npcap from [https://npcap.com/](https://npcap.com/)
   - Run the installer with default settings

## Usage

1. Open a command prompt/terminal with administrator privileges
2. Navigate to the project directory:
```bash
cd path/to/web_debuggerIDE1
```
3. Run the analyzer:
```bash
python network_analyzer_gui.py
```

## Interface Guide

- **Main View**: Displays real-time packet information
- **Network Statistics**: Shows protocol distribution and traffic patterns
- **Network Forensics**: Provides detailed analysis of suspicious traffic
- **Protocol Analysis**: Maps active network connections to processes

## Troubleshooting

- If you get permission errors, make sure you're running as administrator
- For packet capture issues, verify that Npcap is properly installed
- Check your firewall settings if no packets are being captured

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements!

## License

This project is open source, free to use and modify. Please credit the original source if you redistribute it.
