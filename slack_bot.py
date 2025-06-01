import os
import time
from datetime import datetime, timedelta  # For scheduling
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Load .env file
load_dotenv()

#the credentials and channel info from environment variables
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID_FOR_ASSIGNMENT")

# This dictionary will hold onto message timestamps (ts) and scheduled message IDs
ephemeral_message_store = {}


def main():
    """
    Main function to orchestrate the Slack messaging operations.
    """
    print("Starting the Slack messaging assignment script...")

    if not SLACK_BOT_TOKEN:
        print("CRITICAL ERROR: SLACK_BOT_TOKEN is not set. Check .env file.")
        return  # Stop execution if no token
    if not SLACK_CHANNEL_ID:
        print("CRITICAL ERROR: SLACK_CHANNEL_ID_FOR_ASSIGNMENT is not set. Check  .env file.")
        return  # Stop execution if no channel ID

    # Initialize the Slack WebClient
    # This is our main connection to the Slack API
    try:
        slack_client = WebClient(token=SLACK_BOT_TOKEN)
        print("Successfully initialized Slack WebClient.")

        # Let's test the authentication to make sure the token is valid
        auth_response = slack_client.auth_test()
        print(
            f"Authentication successful for bot: {auth_response.get('user', 'Unknown User')} on team: {auth_response.get('team', 'Unknown Team')}")
    except SlackApiError as e:
        print(f"Error during Slack client initialization or auth_test: {e.response['error']}")
        print("Please check your SLACK_BOT_TOKEN and network connection.")
        return
    except Exception as e:
        print(f"An unexpected error occurred during setup: {e}")
        return

    # --- Task 1: Send a Message ---
    print("\n--- OPERATION: Sending a Message ---")
    current_time_str = datetime.now().strftime('%H:%M:%S')
    message_content_original = (
        f"Hello there! I'm 'AssignmentBot', created by an aspiring intern. "
        f"This message was posted at {current_time_str}."
        f"Watch this space!"
    )
    sent_ts = send_slack_message(slack_client, SLACK_CHANNEL_ID, message_content_original)
    if sent_ts:
        ephemeral_message_store["first_message_ts"] = sent_ts
        print(f"Stored TS for sent message: {sent_ts}")
    else:
        print("Failed to send the initial message. Some operations might be skipped.")

    time.sleep(1)

    # --- Task 2: Schedule a Message ---
    print("\n--- OPERATION: Scheduling a Message ---")
    # Schedule a message for 2 minutes
    schedule_time = datetime.now() + timedelta(minutes=2)
    post_at_timestamp = int(schedule_time.timestamp())
    #Scheduled message
    scheduled_message_text = (
        f"'AssignmentBot' here again. This is a scheduled message, "
        f"due to arrive around {schedule_time.strftime('%H:%M:%S')}. "
        f"I'm learning all about timing with the Slack API!"
    )
    scheduled_id = schedule_slack_message(slack_client, SLACK_CHANNEL_ID, scheduled_message_text, post_at_timestamp)
    if scheduled_id:
        ephemeral_message_store["my_scheduled_message_id"] = scheduled_id
        print(f"Stored ID for scheduled message: {scheduled_id}")

    time.sleep(1)

    # --- Task 3: Retrieve a Message ---
    print("\n--- OPERATION: Retrieving a Message ---")
    if "first_message_ts" in ephemeral_message_store:
        print(f"Attempting to retrieve message with TS: {ephemeral_message_store['first_message_ts']}")
        retrieved_msg = retrieve_one_message(slack_client, SLACK_CHANNEL_ID,
                                             ephemeral_message_store["first_message_ts"])
        if retrieved_msg:
            print(f"Successfully retrieved message. Text: '{retrieved_msg.get('text', 'N/A')}'")
        else:
            print(f"Could not retrieve message with TS: {ephemeral_message_store['first_message_ts']}")
    else:
        print("Skipping message retrieval because 'first_message_ts' was not found (original send likely failed).")

    time.sleep(1)

    # --- Task 4: Edit a Message ---
    print("\n--- OPERATION: Editing a Message ---")
    if "first_message_ts" in ephemeral_message_store:
        edited_time_str = datetime.now().strftime('%H:%M:%S')
        #edited message
        new_text_for_message = (
            f"UPDATE from 'AssignmentBot'! The original message has now been skillfully EDITED at {edited_time_str}. "
            f"Showing off my `chat.update` skills for the internship. 😉"
            f"to be deleted soon"
        )
        was_edited = edit_slack_message(slack_client, SLACK_CHANNEL_ID, ephemeral_message_store["first_message_ts"],
                                        new_text_for_message)
        if was_edited:
            print("Message edit seems successful. Check Slack!")
        else:
            print("Message edit failed.")
    else:
        print("Skipping message edit because 'first_message_ts' was not found.")

    time.sleep(1)

    print("\nPausing for a 5 seconds to observe the edited message in Slack...")
    time.sleep(5)

    # --- Task 5: Delete a Message ---
    print("\n--- OPERATION: Deleting a Message ---")
    if "first_message_ts" in ephemeral_message_store:
        was_deleted = delete_slack_message(slack_client, SLACK_CHANNEL_ID, ephemeral_message_store["first_message_ts"])
        if was_deleted:
            print("Message deletion seems successful. Check Slack!")
        else:
            print("Message deletion failed.")
    else:
        print("Skipping message deletion because 'first_message_ts' was not found.")

    time.sleep(1)

    # --- Delete the Scheduled Message (the schedule itself) ---
    print("\n--- OPERATION: Deleting a Scheduled Message (Cancelling it) ---")
    if "my_scheduled_message_id" in ephemeral_message_store:
        cancelled_schedule = delete_pending_scheduled_message(slack_client, SLACK_CHANNEL_ID,
                                                              ephemeral_message_store["my_scheduled_message_id"])
        if cancelled_schedule:
            print("Attempted to cancel the scheduled message. If successful, it won't post.")
        else:
            print("Failed to cancel the scheduled message. It might still post (e.g., if already posted due to timing).")
    else:
        print("Skipping scheduled message cancellation, ID not found.")

    print("\nAll assigned operations attempted. Script finished.")
    print("Please check your Slack channel to observe the results.")


# Helper functions for Slack operations (These remain largely the same)

def send_slack_message(client: WebClient, channel_id: str, text: str):
    """Posts a message to a Slack channel."""
    try:
        response = client.chat_postMessage(channel=channel_id, text=text)
        print(f"  Successfully sent message to {channel_id}. TS: {response['ts']}")
        return response['ts']
    except SlackApiError as e:
        print(f"  Error sending message: {e.response['error']}")
        print(f"  Full error response: {e.response}")
        return None

def schedule_slack_message(client: WebClient, channel_id: str, text: str, post_at: int):
    """Schedules a message for future delivery."""
    try:
        response = client.chat_scheduleMessage(
            channel=channel_id,
            text=text,
            post_at=post_at
        )
        readable_time = datetime.fromtimestamp(post_at).strftime('%Y-%m-%d %H:%M:%S')
        print(
            f"  Successfully scheduled message. ID: {response['scheduled_message_id']}. Will post at {readable_time}.")
        return response['scheduled_message_id']
    except SlackApiError as e:
        print(f"  Error scheduling message: {e.response['error']}")
        print(f"  Full error response: {e.response}")
        return None

def retrieve_one_message(client: WebClient, channel_id: str, message_ts: str):
    """Retrieves a specific message using its timestamp."""
    try:
        response = client.conversations_history(
            channel=channel_id,
            latest=message_ts,
            inclusive=True,
            limit=1
        )
        if response['messages'] and len(response['messages']) > 0:
            return response['messages'][0]
        else:
            print(f"  Could not find message with TS {message_ts} in channel {channel_id}.")
            return None
    except SlackApiError as e:
        print(f"  Error retrieving message: {e.response['error']}")
        print(f"  Full error response: {e.response}")
        return None

def edit_slack_message(client: WebClient, channel_id: str, message_ts: str, new_text: str):
    """Modifies an existing message."""
    try:
        response = client.chat_update(
            channel=channel_id,
            ts=message_ts,
            text=new_text
        )
        if response['ok']:
            print(f"  Successfully edited message (TS: {message_ts}). New text: '{new_text}'")
            return True
        else:
            print(f"  Failed to edit message (TS: {message_ts}). Response: {response}")
            return False
    except SlackApiError as e:
        print(f"  Error editing message: {e.response['error']}")
        print(f"  Full error response: {e.response}")
        return False

def delete_slack_message(client: WebClient, channel_id: str, message_ts: str):
    """Removes a message from a channel."""
    try:
        response = client.chat_delete(channel=channel_id, ts=message_ts)
        if response['ok']:
            print(f"  Successfully deleted message (TS: {message_ts}).")
            return True
        else:
            print(f"  Failed to delete message (TS: {message_ts}). Response: {response}")
            return False
    except SlackApiError as e:
        print(f"  Error deleting message: {e.response['error']}")
        print(f"  Full error response: {e.response}")
        return False

def delete_pending_scheduled_message(client: WebClient, channel_id: str, scheduled_message_id: str):
    """Deletes a PENDING scheduled message (cancels it)."""
    try:
        response = client.chat_deleteScheduledMessage(
            channel=channel_id,
            scheduled_message_id=scheduled_message_id
        )
        if response['ok']:
            print(f"  Successfully cancelled scheduled message (ID: {scheduled_message_id}).")
            return True
        else:
            print(f"  Failed to cancel scheduled message (ID: {scheduled_message_id}). Response: {response}")
            return False
    except SlackApiError as e:
        print(f"  Error cancelling scheduled message: {e.response['error']}")
        print(f"  Full error response: {e.response}")
        return False

if __name__ == "__main__":
    main()