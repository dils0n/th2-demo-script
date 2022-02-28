from __future__ import print_function

import datetime
import logging
import time

from google.protobuf.timestamp_pb2 import Timestamp

from custom import support_functions as sf


def scenario(factory):
    # Storing grpc Timestamp of script start.
    report_start_timestamp = Timestamp()
    report_start_timestamp.GetCurrentTime()

    # Sending request to estore. Creation of the root Event for all cases performed.

    # CASE 1
    parent_id = sf.create_event_id()

    sf.send_event(
        factory=factory,
        start_timestamp=report_start_timestamp,
        event_id=sf.create_event_id(),
        parent_id=parent_id,
        name='CASE_1',
        status='FAILED')

    sf.send_root(
        factory=factory,
        start_timestamp=report_start_timestamp,
        event_id=parent_id,
        name='CASE_1',
        status='SUCCESS')

    # CASE 2
    parent_id = sf.create_event_id()
    sf.send_event(
        factory=factory,
        start_timestamp=report_start_timestamp,
        event_id=sf.create_event_id(),
        parent_id=parent_id,
        name='CASE_2',
        status='FAILED')

    time.sleep(1)

    sf.send_root(
        factory=factory,
        start_timestamp=report_start_timestamp,
        event_id=parent_id,
        name='CASE_2',
        status='SUCCESS')

    # CASE 3
    parent_id = sf.create_event_id()
    sf.send_event(
        factory=factory,
        start_timestamp=report_start_timestamp,
        event_id=sf.create_event_id(),
        parent_id=parent_id,
        name='CASE_3',
        status='FAILED')

    # time exceeding the waiting time parent_event_id
    time.sleep(30)

    sf.send_event(
        factory=factory,
        start_timestamp=report_start_timestamp,
        event_id=sf.create_event_id(),
        parent_id=parent_id,
        name='CASE_3',
        status='FAILED')

    sf.send_root(
        factory=factory,
        start_timestamp=report_start_timestamp,
        event_id=parent_id,
        name='CASE_3',
        status='SUCCESS')


if __name__ == '__main__':
    logging.basicConfig(filename=time.asctime().replace(':', '-') + ' script.log',
                        level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    factory = sf.connect(config_path="./configs/")

    try:
        start_datetime = datetime.datetime.now()
        scenario(factory)
        time.sleep(10)
        finish_datetime = datetime.datetime.now()

        print(F"start datetime: {start_datetime}")
        print(F"finish datetime: {finish_datetime}")

    finally:
        factory['factory'].close()
