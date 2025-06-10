# Honey-pot

markdown
# SSH Honeypot

A simple SSH honeypot designed to log authentication attempts and commands from potential attackers. This project mimics a basic Linux shell to deceive attackers while capturing their activities.

## Features

- Simulates an SSH login prompt (username/password)
- Logs all authentication attempts (both successful and failed)
- Mimics common shell commands with fake responses
- Stores session data in both log files and Excel format
- Multi-threaded to handle multiple connections
- Password input masking (shows asterisks while typing)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ssh-honeypot.git
   cd ssh-honeypot
Install required dependencies:

bash
pip install openpyxl
Usage
Run the honeypot:

bash
python honeypot.py
The honeypot will:

Listen on port 2222 by default (configurable in the code)

Create two log files:

honeypot.log - Text log of all activity

honeypot_log.xlsx - Structured Excel log with session details

Configuration
You can modify these variables in the code:

HOST and PORT - Binding address and port

FAKE_SHELL_RESPONSES - Customize command responses

Logging format and handlers

Data Collection
The honeypot collects:

Attacker IP address and connection time

Username and password attempts

All commands executed during the session

Timestamps for all activities

Security Warning
⚠️ Important Security Note:

This honeypot is designed for research/educational purposes only

Do not run on production systems or networks

Exposing this to the internet will attract malicious traffic

Ensure proper firewall rules and isolation

License
MIT License - See LICENSE file for details

Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

text

You can customize this further by:
1. Adding screenshots of sample logs
2. Including more detailed setup instructions
3. Adding a "Detection Avoidance" section if you've implemented any features for that
4. Including sample output/examples

Would you like me to add any additional sections or modify any part of this README?
