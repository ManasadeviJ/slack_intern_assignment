# slack_intern_assignment

# Slack API Messaging Demo - Internship Assignment

Hi there! This project is my submission for the internship assignment focusing on Slack API messaging functionalities. I've created a Python script that interacts with a Slack developer sandbox to perform various messaging operations. It's been a great learning experience working with the Slack SDK!

## What This Script Does

The Python script (`slack_bot.py`) demonstrates the following core capabilities:

1.  **Authentication:** Connects to the Slack API using a Bot User OAuth Token.
2.  **Sending Messages:** Posts a custom message directly to a specified Slack channel.
3.  **Scheduling Messages:** Schedules a different custom message for future delivery in the same channel.
4.  **Retrieving Messages:** Fetches the details of the first message that was sent.
5.  **Editing Messages:** Modifies the content of that first sent message.
6.  **Deleting Messages:** Removes the (now edited) first message from the channel.
7.  **Managing Scheduled Messages:** Attempts to cancel the pending scheduled message before it's due to post.

I've tried to make the bot's messages a little engaging to show some personality!

## Setting Up Your Own Sandbox to Run This

To get this script running in your own Slack developer sandbox, here's what I did (and what you'll need to do):

1.  **Create a Slack Workspace (Sandbox):**
    *   If you don't have one already, create a new, free Slack workspace. This will be your safe testing ground.

2.  **Create a Slack App:**
    *   Go to the [Slack API site](https://api.slack.com/apps) and create a new app "From scratch."
    *   Name it something like "MyTestBot" and associate it with your sandbox workspace.

3.  **Configure Bot Token Scopes:**
    *   In your app's settings, navigate to "OAuth & Permissions."
    *   Under "Bot Token Scopes," add the following permissions (scopes):
        *   `chat:write` (to send, edit, delete messages, and manage scheduled messages)
        *   `channels:history` (to retrieve messages from public channels)
        *   *(If testing in private channels, you might need `groups:history`)*

4.  **Install App & Get Token:**
    *   Install your app to your sandbox workspace.
    *   After installation, copy the **Bot User OAuth Token** (it starts with `xoxb-`). This is your `SLACK_BOT_TOKEN`.

5.  **Get Channel ID:**
    *   In your sandbox workspace, create a public channel for testing (e.g., `#bot-testing-zone`).
    *   Invite your bot to this channel (e.g., `/invite @MyTestBot`).
    *   To get the Channel ID: Right-click the channel name in Slack, select "Copy Link." The ID is the part that looks like `C0XXXXXXXXX` in the copied URL. This will be your `SLACK_CHANNEL_ID_FOR_ASSIGNMENT`.

## How to Run the Script

Once you have your sandbox, bot token, and channel ID:

1.  **Clone/Download:**
    *   Get the `slack_bot.py` script (and this `README.md`).

2.  **Python Environment (Recommended):**
    *   It's best to use a virtual environment. Make sure you have Python 3.7+ installed.
    ```bash
    python -m venv venv
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows (Command Prompt):
    # venv\Scripts\activate.bat
    ```

3.  **Install Dependencies:**
    *   The script relies on `slack_sdk` and `python-dotenv`.
    ```bash
    pip install slack_sdk python-dotenv
    ```

4.  **Create `.env` File:**
    *   In the same directory as `slack_bot.py`, create a file named `.env`.
    *   Add your token and channel ID to this file like so:
        ```env
        SLACK_BOT_TOKEN="xoxb-YOUR_BOT_TOKEN_HERE"
        SLACK_CHANNEL_ID_FOR_ASSIGNMENT="C_YOUR_CHANNEL_ID_HERE"
        ```
    *   **Important:** Replace the placeholders with your actual token and channel ID!

5.  **Run the Script:**
    ```bash
    python slack_bot.py
    ```

6.  **Observe!**
    *   Watch the terminal output for status messages from the script.
    *   Check your designated Slack channel to see the "AssignmentBot" in action – sending, editing, and deleting messages, and managing its schedule!

## A Few Notes on the Implementation

*   The script uses `python-dotenv` to keep the Slack token and channel ID out of the main codebase (good for security!).
*   I've used a simple Python dictionary (`ephemeral_message_store`) to keep track of message timestamps and scheduled message IDs during a single run of the script. For a more permanent application, a database would be a better choice for this.
*   The script includes `time.sleep()` calls to make the sequence of operations a bit more observable and to give Slack's API a moment between calls. There's also an optional longer pause after editing so you can see the edited message in Slack before it's deleted.
*   Error handling for API calls is included using `try...except SlackApiError`.

---

Thanks for the opportunity to work on this assignment! I'm keen to learn more.
