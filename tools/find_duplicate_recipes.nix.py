#!/usr/bin/env nix-shell
#! nix-shell -p python3 -i python3
import os
import json

id_map = {}
for filepath in [
    os.path.join(root, file)
    for root, _, files in os.walk(".")
    for file in files
    if file.endswith(".json")
]:
    with open(filepath, mode="r", encoding="utf-8") as read_file:
        data = json.load(read_file)
        if isinstance(data, list):
            for item in [
                item
                for item in data
                if isinstance(item, dict)
                and "type" in item
                and item["type"] == "recipe"
                and "result" in item
            ]:
                id_map.setdefault(item["result"], []).append(filepath)
for id, files in id_map.items():
    if len(files) > 1:
        print(f"Duplicate recipe result ID: {id}")
        for fname in files:
            print(fname)
