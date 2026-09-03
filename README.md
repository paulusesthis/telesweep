# TELESWEEP

### Telegram Account Cleanup & Organization Tool

TELESWEEP is a Python-based Telegram account management tool built with Telethon. It provides a simple terminal interface for reviewing and cleaning up groups, channels, and bot chats associated with your Telegram account.

## Features

* View all groups in your Telegram account
* View all channels in your Telegram account
* View all bot chats
* Leave specific groups
* Leave specific channels
* Delete specific bot chats
* Search for groups, channels, and bots
* Select individual items
* Select multiple items using comma-separated numbers
* Select ranges such as `2-19`
* Combine multiple ranges such as `2-19, 21-28, 30-87`
* Leave all groups
* Leave all channels
* Delete all bot chats
* Confirmation before destructive operations
* Flood wait handling
* Progress tracking
* Local Telegram session storage
* Environment variable support for Telegram API credentials

## Requirements

Before installing TELESWEEP, make sure you have:

* Python 3.9 or newer
* A Telegram account
* Telegram API credentials
* Git, if you are cloning the repository

## 1. Get Your Telegram API Credentials

TELESWEEP uses Telegram's official API through Telethon. You need an `API ID` and `API Hash` to connect to your Telegram account.

Open Telegram's official API development page:

https://my.telegram.org/

Sign in using the phone number associated with your Telegram account.

After signing in:

1. Select **API development tools**.
2. If you have not created an application before, complete the application form.
3. Telegram will provide you with:

   * `api_id`
   * `api_hash`

<!-- SCREENSHOT: Telegram API development tools page showing where API ID and API Hash are displayed -->

Keep your API Hash private. Do not publish it on GitHub or share it publicly.

## 2. Clone the Repository

Open a terminal and clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
```

Enter the project directory:

```bash
cd TELESWEEP
```

<!-- SCREENSHOT: Terminal showing the repository being cloned -->

## 3. Create a Virtual Environment

Creating a virtual environment keeps TELESWEEP's Python dependencies isolated from the rest of your system.

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### macOS and Linux

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Once activated, your terminal should indicate that the virtual environment is active.

## 4. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

The main dependencies are:

* Telethon
* Colorama
* python-dotenv

## 5. Create Your Environment File

TELESWEEP does not store your Telegram API credentials directly inside the Python source code.

Instead, create a file named:

```text
.env
```

in the root of the project.

Your project should look like this:

```text
TELESWEEP/
├── telesweep.py
├── requirements.txt
├── .env.example
├── .gitignore
└── .env
```

Copy the contents of `.env.example` into `.env`.

Example:

```env
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=your_api_hash_here
```

Replace the placeholder values with your own Telegram API credentials.

Do not add quotation marks around the values.

For example:

```env
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=0123456789abcdef0123456789abcdef
```

<!-- SCREENSHOT: VS Code showing the .env file with the API ID and API Hash fields filled in. Blur or hide the actual credentials before publishing the screenshot. -->

## 6. Check Your .gitignore

Your `.gitignore` should prevent sensitive files from being uploaded to GitHub.

A recommended `.gitignore` is:

```gitignore
.env
*.session
*.session-journal

__pycache__/
*.py[cod]

venv/
.venv/
env/
```

The following files should never be committed:

```text
.env
telegram_session.session
telegram_session.session-journal
```

Your `.env` contains your API credentials.

Your `.session` file contains your authenticated Telegram session.

Both should remain private.

## 7. Run TELESWEEP

Once everything is configured, start the application:

```bash
python telesweep.py
```

On the first run, Telethon will ask you to authenticate your Telegram account.

You will normally be asked for:

1. Your Telegram phone number
2. The login code Telegram sends you
3. Your two-step verification password, if enabled

After successful authentication, Telethon creates a local session file.

For example:

```text
telegram_session.session
```

You should not upload this file to GitHub.

<!-- SCREENSHOT: TELESWEEP first-run authentication prompt -->

## 8. Using the Main Menu

After connecting, TELESWEEP scans your account and displays an overview of the available groups, channels, and bot chats.

The main menu provides:

```text
[01] Leave specific groups
[02] Leave specific channels
[03] Delete specific bot chats
[04] Search group/channel/bot
[05] Leave ALL groups
[06] Leave ALL channels
[07] Delete ALL bot chats
[08] Refresh account
[09] Exit
```

<!-- SCREENSHOT: TELESWEEP main control panel -->

## 9. Selecting Items

TELESWEEP supports several selection formats.

### Select one item

```text
2
```

### Select multiple individual items

```text
2,5,8
```

### Select a range

```text
2-19
```

### Select multiple ranges

```text
2-19, 21-28, 30-87, 89-240
```

Spaces are allowed.

The numbers correspond to the numbered items displayed by TELESWEEP.

## 10. Search

The search function allows you to search across:

* Groups
* Channels
* Bot chats

Select:

```text
[04] Search group/channel/bot
```

Enter part of the name you are looking for.

For example:

```text
Search: crypto
```

TELESWEEP will display matching results and allow you to select them using the same number and range system.

## 11. Confirmation

TELESWEEP requires confirmation before performing an operation that changes your Telegram account.

Before an operation is executed, the selected items are displayed.

You must type:

```text
LEAVE
```

to confirm.

Anything else cancels the operation.

This is intentional to reduce accidental bulk actions.

## 12. What TELESWEEP Does

TELESWEEP uses Telegram's API through Telethon to manage the selected dialogs.

When leaving a group or channel, TELESWEEP removes your account from that group or channel.

When deleting a bot chat, TELESWEEP removes the bot conversation from your dialog list.

TELESWEEP does not delete your Telegram account.

It also does not delete the groups or channels themselves.

## 13. Telegram Session File

After authentication, Telethon creates a session file:

```text
telegram_session.session
```

This allows TELESWEEP to reuse your authenticated session instead of requiring you to log in every time.

Do not share this file.

Treat it as sensitive.

If you delete the session file, TELESWEEP will require authentication again the next time it runs.

## 14. Security

Never publish your:

```text
TELEGRAM_API_ID
TELEGRAM_API_HASH
telegram_session.session
```

Do not place your API credentials directly inside `telesweep.py`.

Use the `.env` file instead.

The `.env` file is intentionally excluded from Git through `.gitignore`.

### Important

If you accidentally publish your API credentials or Telegram session file to a public repository, remove the sensitive information immediately and take appropriate steps to invalidate or replace compromised credentials.

## 15. Updating TELESWEEP

If you have already cloned the repository and want to get the latest version:

```bash
git pull
```

Then update the dependencies if necessary:

```bash
pip install -r requirements.txt --upgrade
```

Your local `.env` and `.session` files should remain untracked and should not be affected by normal Git updates.

## 16. Project Structure

```text
TELESWEEP/
│
├── telesweep.py
│   Main application
│
├── requirements.txt
│   Python dependencies
│
├── .env.example
│   Example environment configuration
│
├── .gitignore
│   Prevents sensitive and generated files from being committed
│
├── README.md
│   Documentation
│
└── .env
    Local API credentials
    Not committed to Git
```

## 17. Troubleshooting

### `ModuleNotFoundError`

If you see an error such as:

```text
ModuleNotFoundError: No module named 'telethon'
```

install the dependencies:

```bash
pip install -r requirements.txt
```

### API credentials not found

Make sure:

* The file is named `.env`
* It is located in the same project directory as `telesweep.py`
* The variables are named correctly
* The values are valid

Your `.env` should contain:

```env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
```

### TELESWEEP asks me to log in again

If your session file was deleted, moved, or is no longer available, Telethon will require authentication again.

Run:

```bash
python telesweep.py
```

and complete the authentication process.

### Flood wait

Telegram may temporarily restrict how quickly an application can perform certain actions.

TELESWEEP detects Telegram flood-wait responses and waits for the period specified by Telegram before continuing.

Avoid repeatedly starting large cleanup operations in a short period.

## 18. Development

To contribute to TELESWEEP:

1. Fork the repository.
2. Clone your fork.
3. Create a virtual environment.
4. Install the dependencies.
5. Create your own `.env`.
6. Make your changes.
7. Test the application.
8. Commit your changes.
9. Open a pull request.

Never include your `.env` or Telegram session files in a pull request.

## 19. Disclaimer

TELESWEEP is provided for personal Telegram account management and organization.

Use the tool responsibly and in accordance with Telegram's terms and policies.

You are responsible for the actions performed on your Telegram account.

## License

Add your preferred license here.

For example:

```text
MIT License
```

---

**TELESWEEP**

Telegram Account Cleanup & Organization Tool

Made by Paul

Telegram: @vibezat1k
