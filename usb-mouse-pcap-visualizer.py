#!/usr/bin/env python
# coding:utf-8

import argparse
import struct
import sys
import enum
import matplotlib.pyplot as plt
import numpy as np
import pyshark
import loguru

from typing import List

class Opcode(enum.Enum):
    LEFT_BUTTON_HOLDING = 0b00000001
    RIGHT_BUTTON_HOLDING = 0b00000010


class MouseSnapshot:
    def __init__(self, timestamp, x, y, left_button_holding, right_button_holding):
        self.timestamp = timestamp
        self.x = x
        self.y = y
        self.left_button_holding = left_button_holding
        self.right_button_holding = right_button_holding


class MouseEmulator:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.left_button_holding = False
        self.left_button_holding = False

    def move(self, x, y):
        loguru.logger.debug(f"move(x={x}, y={y})")
        self.x += x
        self.y -= y

    def set_left_button(self, state):
        loguru.logger.debug(f"set_left_button(state={state})")
        self.left_button_holding = state

    def set_right_button(self, state):
        loguru.logger.debug(f"set_right_button(state={state})")
        self.right_button_holding = state

    def snapshot(self, timestamp):
        return MouseSnapshot(timestamp, self.x, self.y, self.left_button_holding, self.right_button_holding)


class MouseTracer:
    def __init__(self):
        self.snapshots: List[MouseSnapshot] = []

    def add(self, snapshot: MouseSnapshot):
        self.snapshots.append(snapshot)


def load_pcap(filepath):
    loguru.logger.debug(f"load_pcap(filepath={filepath})")
    cap = pyshark.FileCapture(filepath)
    for packet in cap:
        if hasattr(packet, 'DATA'):
            usbhid_data = packet.DATA.get_field("usbhid_data")
            usb_capdata = packet.DATA.get_field("usb_capdata")
            timestamp = packet.sniff_timestamp
            for data in [usbhid_data, usb_capdata]: 
                if data:
                    yield (timestamp, data)


def parse_packet(payload):
    items = [struct.unpack('b', bytes.fromhex(i))[0]
             for i in payload.split(":")]

    state, movement_x, movement_y = 0, 0, 0

    if len(items) == 4:
        state, movement_x, movement_y, _ = items

    if len(items) == 8:
        state, _, movement_x, _, movement_y, _, _, _ = items

    left_button_holding = state & Opcode.LEFT_BUTTON_HOLDING.value != 0
    right_button_holding = state & Opcode.RIGHT_BUTTON_HOLDING.value != 0

    return movement_x, movement_y, left_button_holding, right_button_holding


def snapshot_mouse(filepath):
    mouse_emulator = MouseEmulator()
    for timestamp, data in load_pcap(filepath):
        mx, my, lbh, rbh = parse_packet(data)
        mouse_emulator.move(mx, my)
        mouse_emulator.set_left_button(lbh)
        mouse_emulator.set_right_button(rbh)
        yield mouse_emulator.snapshot(timestamp)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", help="Path to the input pcap file.", required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    mt = MouseTracer()
    xs = []
    ys = []
    colors = []
    alphas = []
    for snapshot in snapshot_mouse(args.input_file):
        mt.add(snapshot)
        color = "red" if snapshot.left_button_holding else "grey"
        color = "blue" if snapshot.right_button_holding else color
        alpha = 1 if snapshot.left_button_holding or snapshot.right_button_holding else 0.1
        xs.append(snapshot.x)
        ys.append(snapshot.y)
        colors.append(color)
        alphas.append(alpha)

    plt.scatter(xs, ys, c=colors, alpha=alphas)
    plt.show()


if __name__ == "__main__":
    main()
