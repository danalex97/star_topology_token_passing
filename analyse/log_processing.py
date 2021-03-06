import os

from log_entries import LogEntry
from log_entries import BroadcastSentEntry
from log_entries import BroadcastRecvEntry
from log_entries import PrioritySentEntry
from log_entries import NodeJoinEntry
from log_entries import PriorityRecvEntry
from log_entries import BroadcastBaseRequestEntry

def process_entry(log_raw_entry):
    def try_entry(entry_type, log_raw_entry):
        try:
            return entry_type(log_raw_entry)
        except:
            return None

    entry_types = [
        NodeJoinEntry,
        BroadcastSentEntry,
        BroadcastBaseRequestEntry,
        BroadcastRecvEntry,
        PrioritySentEntry,
        PriorityRecvEntry,
        LogEntry
    ]
    for entry_type in entry_types:
        entry = try_entry(entry_type, log_raw_entry)
        if entry is not None:
            return entry
    return None

def get_log(log_file_path):
    script_dir = os.path.dirname(__file__)
    abs_log_file_path = os.path.join(script_dir, '..', log_file_path)

    with open(abs_log_file_path, "r") as log_file:
        log_raw_entries = log_file.read().split("\n")

        log_entries = map(process_entry, log_raw_entries)
        log_entries = filter(lambda x: x is not None, log_entries)

        return list(log_entries)

global lines_per_file
lines_per_file = {}

def group_by(entries, criteria):
    grouped = {}
    for entry in entries:
        if criteria(entry) not in grouped:
            grouped[criteria(entry)] = []
        grouped[criteria(entry)].append(entry)
    return grouped

def filter_entries(log_entries, log_type):
    return [e for e in log_entries if isinstance(e, log_type)]
