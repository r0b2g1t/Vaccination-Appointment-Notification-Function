import apprise
import azure.functions as func
from azure.storage.queue import QueueClient
import datetime 
import json
import logging
import os
import requests


def main(mytimer: func.TimerRequest) -> None:
    url = 'https://www.startupuniverse.ch/api/1.1/de/counters/getAll/_iz_sachsen'
    vac_center_id = os.environ['VAC_CENTER_ID']
    telegram = 'tgram://{}/{}'.format(
        os.environ['TELEGRAM_API_TOKEN'],
        os.environ["TELEGRAM_GROUP_ID"])
    connection_string = os.environ['STORAGE_QUEUE_CONNECTION_STRING']
    storage_account_queue_name = os.environ['STORAGE_ACCOUNT_QUEUE_NAME']

    resp = requests.get(url)

    counter = resp.json()['response']['data'][vac_center_id]['counteritems'][0]['val']

    raw_dates = json.loads(json.loads(resp.content)['response']['data'][vac_center_id]['counteritems'][0]['val_s'])

    date_list = []

    for i in range(len(raw_dates)):
        date = datetime.datetime.fromtimestamp(raw_dates[i]['d'])
        date = date.strftime("%d.%m.%Y")
        entry ='{} at {}'.format(raw_dates[i]['c'], date)
        date_list.append(entry)

    body = ('\n'.join(map(str, date_list)))

    queue = QueueClient.from_connection_string(
        conn_str=connection_string,
        queue_name=storage_account_queue_name)

    messages = queue.receive_messages()

    slot_changes = False

    for message in messages:
        if body not in message.content:
            slot_changes = True
            logging.info("Slot changes!")
        queue.delete_message(message)

    queue.send_message(body)        

    apobj = apprise.Apprise()
    apobj.add(telegram)

    if counter != 0 and slot_changes:
        logging.info("Send message!")
        apobj.notify(title='{} Free slot available!'.format(counter), body=body)
