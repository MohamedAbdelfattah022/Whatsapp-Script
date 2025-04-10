# WhatsApp Automation Script

This Python script automates sending WhatsApp messages to multiple recipients using WhatsApp Web. It's designed to process phone numbers from CSV/Excel files and track message delivery status.

## Features

- Reads phone numbers from CSV or Excel files
- Validates phone numbers before processing
- Tracks processed numbers to avoid duplicates
- Logs successful deliveries and errors
- Implements rate limiting to prevent blocking
- Uses Microsoft Edge WebDriver for automation

## Requirements

- Python 3.x
- Microsoft Edge browser
- Edge WebDriver (msedgedriver.exe)
- Required Python packages (see requirements.txt):
  - selenium
  - pandas

## Setup

1. Make sure Microsoft Edge is installed
2. Place `msedgedriver.exe` in the project directory
3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Prepare your input file (CSV or Excel) with a "Phone Number" column
2. Configure your message in the script
3. Run the script:
   ```
   python refactored_script.py
   ```
4. Scan the WhatsApp Web QR code when prompted
5. The script will process the numbers automatically

## Logs

The script generates several log files:
- `whatsapp_log.log`: General operation logs
- `invalid_numbers.log`: Records invalid phone numbers
- `processed_numbers.txt`: Tracks successfully processed numbers

## Note

This script is specifically configured for Egyptian phone numbers (+20). Modify the validation pattern in the code if you need to support different formats.