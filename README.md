# Vaccination Appointment Notification Function
The repository provides an Azure Function App which checks the vaccination dashboard for Saxony in Germany and sends a notification via a Telegram Bot to a specific user or group.

The project is based on three components, a storage account that passes the statuses between the function runs, the function app that takes care of checking the dates and the last component, the Telegram bot that informs the user or the group.

## Function Components
The function uses the following libraries:

### Apprise
The [Apprise](https://github.com/caronc/apprise/wiki/Notify_telegram) library is used for notification via Telegram.

### Azure-Storage-Queue
This is used to perform the communication with the storage account.

### Requests
To query the available dates the Library Requests is used.

## Function App Variables
The following variables needs to be set for running the App on Azure:

| Variable Name | Description |
| ------------- |-------------|
| TELEGRAM_API_TOKEN | Telegram Bot API Token |
| TELEGRAM_GROUP_ID | Telegram User or Group ID to be notify |
| STORAGE_QUEUE_CONNECTION_STRING | Azure Storage Account connection string |
| STORAGE_ACCOUNT_QUEUE_NAME | Azure Storage Account State Queue Name needs to be created before |
| VAC_CENTER_ID |ID of the vaccination center which will be checked |

## Telegram Bot
To run the function app a Telegram bot is needed. The creation is also explained in the [Apprise documentation](https://github.com/caronc/apprise/wiki/Notify_telegram).