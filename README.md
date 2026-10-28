# Birthday Email Automation

A lightweight Python automation that checks a CSV file of birthdays each day and, when someone's birthday matches today's date, sends them a personalised greeting by email.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Automating with GitHub Actions](#automating-with-github-actions)
- [Customising Letter Templates](#customising-letter-templates)
- [Security Notes](#security-notes)
- [Troubleshooting](#troubleshooting)
- [Known Limitations and Future Improvements](#known-limitations-and-future-improvements)
- [License](#license)

---

## Overview

Remembering birthdays and writing a message each time is repetitive. This project removes that effort: store your contacts' birthdays in a CSV file, run the script daily, and it handles the rest, picking a random letter template, inserting the recipient's name, and sending the email through Gmail's SMTP server.

## Features

- **CSV-driven data**: manage birthdays in a simple spreadsheet-friendly file.
- **Personalised messages**: the recipient's name is inserted automatically.
- **Randomised templates**: one of several letter templates is chosen at random, so greetings stay varied.
- **Secure SMTP connection**: uses SSL (port 465) via Python's `ssl` default context.
- **Credentials kept out of code**: the email address and password are read from environment variables.
- **Scheduler-ready**: designed to run once per day, locally or through GitHub Actions.

## How It Works

1. The script reads your sender credentials from environment variables.
2. It determines today's month and day.
3. It loads `birthdays.csv` and builds a lookup keyed by `(month, day)`.
4. If today matches an entry, it selects a random template from `letter_templates/` and replaces the `[NAME]` placeholder with the person's name.
5. It connects to Gmail's SMTP server over SSL and sends the email with the subject **"Happy Birthday!"**.
6. If nobody has a birthday today, the script exits without sending anything.

## Project Structure

```
birthday-email-automation-project/
├── .github/
│   └── workflows/          # GitHub Actions workflow configuration
├── letter_templates/       # Letter templates (letter_1.txt, letter_2.txt, letter_3.txt)
├── birthdays.csv           # Birthday data
├── main.py                 # Main script
├── requirements.txt        # Python dependencies
└── README.md
```

## Prerequisites

- Python 3.8 or later
- A Gmail account with 2-Step Verification enabled
- A Gmail **App Password** (a regular account password will not work with SMTP; see [Configuration](#configuration))

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Armish11/birthday-email-automation-project.git
   cd birthday-email-automation-project
   ```

2. **(Recommended) Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS / Linux
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### 1. Gmail App Password

1. Enable 2-Step Verification on your Google account.
2. Go to **Google Account → Security → App passwords**.
3. Generate a new app password and copy the 16-character code.

### 2. Environment variables

The script expects two environment variables:

| Variable      | Description                                  |
| ------------- | -------------------------------------------- |
| `MY_EMAIL`    | The Gmail address the emails are sent from   |
| `MY_PASSWORD` | The Gmail App Password generated above       |

Set them in your terminal before running the script:

```bash
# macOS / Linux
export MY_EMAIL="your_email@gmail.com"
export MY_PASSWORD="your_app_password"

# Windows (PowerShell)
$env:MY_EMAIL="your_email@gmail.com"
$env:MY_PASSWORD="your_app_password"
```

### 3. Birthday data

Edit `birthdays.csv` using the following columns:

```csv
name,email,year,month,day
Jane Doe,jane@example.com,1995,4,12
John Smith,john@example.com,1990,11,3
```

| Column  | Description                          |
| ------- | ------------------------------------ |
| `name`  | Recipient's name (used in the letter) |
| `email` | Recipient's email address            |
| `year`  | Birth year                           |
| `month` | Birth month as a number (1–12)      |
| `day`   | Day of the month (1–31)              |

> The script matches on `month` and `day` only; `year` is stored for reference.

### 4. Letter templates

Templates live in `letter_templates/` and are named `letter_1.txt`, `letter_2.txt`, and `letter_3.txt`. Use `[NAME]` wherever the recipient's name should appear.

## Usage

Run the script from the project root:

```bash
python main.py
```

- If today matches a birthday in the CSV, an email is sent to that person.
- If there is no match, nothing happens.

To test it, temporarily add a row to `birthdays.csv` with today's month and day and your own email address.

## Automating with GitHub Actions

The repository includes a workflow directory at `.github/workflows/` so the script can run on a schedule without your computer being on. To use it:

1. In your repository, go to **Settings → Secrets and variables → Actions**.
2. Add two repository secrets: `MY_EMAIL` and `MY_PASSWORD`.
3. Make sure the workflow passes those secrets to the script as environment variables.
4. Enable GitHub Actions for the repository, then trigger the workflow manually once to confirm it works.

> **Tip:** Scheduled GitHub Actions run on UTC time. Adjust the cron expression if you need the email to go out at a specific local time.

For local scheduling instead, you can use `cron` (macOS / Linux) or Task Scheduler (Windows) to run `python main.py` once a day.

## Customising Letter Templates

Open any file in `letter_templates/` and edit the text. Example:

```text
Dear [NAME],

Wishing you a very happy birthday! May your day be filled with joy,
laughter, and everything you love.

Warm regards,
Your Name
```

To add more templates, create additional files and update the random range in `main.py` (currently `random.randint(1, 3)`) to match the number of templates.

## Security Notes

- **Never commit credentials.** Keep your email and App Password in environment variables or repository secrets only.
- Use a Gmail **App Password**, not your main account password.
- Birthday data contains personal information. Consider keeping the repository private if `birthdays.csv` holds real contacts.

## Troubleshooting

| Problem | Likely cause and fix |
| ------- | -------------------- |
| `KeyError: 'MY_EMAIL'` | The environment variables are not set in the current session. |
| `SMTPAuthenticationError` | Wrong credentials, or an App Password is required. Confirm 2-Step Verification is on and use an App Password. |
| `FileNotFoundError` for a letter or the CSV | Run the script from the project root so relative paths resolve. |
| No email received | Check the spam folder, and confirm the CSV month/day match today's date. |
| Connection timeout | Verify your network allows outbound connections on port 465. |

## Known Limitations and Future Improvements

- If several people share the same birthday, only one is currently matched, because entries are keyed by `(month, day)`. Supporting multiple recipients per day would be a worthwhile improvement.
- The SMTP server is hard-coded to Gmail.
- The email subject is fixed as "Happy Birthday!".
- Ideas for the future: HTML emails, configurable SMTP settings, logging, and automated tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Author:** [Armish11](https://github.com/Armish11)
