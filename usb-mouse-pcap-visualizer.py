#!/usr/bin/env python
# coding:utf-8

import argparse
import struct
from enum import Enum

import matplotlib.pyplot as plt
import numpy as np
import pyshark


class Opcode(Enum):
    LEFT_BUTTON_HOLDING = 0b00000001
    RIGHT_BUTTON_HOLDING = 0b00000010


class MouseEmulator:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.left_button_holding = False
        self.left_button_holding = False

    def move(self, x, y):
        self.x += x
        self.y -= y

    def set_left_button(self, state):
        self.left_button_holding = state

    def set_right_button(self, state):
        self.right_button_holding = state

    def snapshot(self):
        return (self.x, self.y, self.left_button_holding, self.right_button_holding)


class MouseTracer:
    def __init__(self):
        self.snapshots = []

    def add(self, snapshot):
        self.snapshots.append(snapshot)


def load_pcap(filepath):
    cap = pyshark.FileCapture(filepath)
    for packet in cap:
        if hasattr(packet, 'usb') and hasattr(packet, 'DATA') and hasattr(packet.DATA, 'usb_capdata'):
            yield packet.DATA.usb_capdata


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
    for i in load_pcap(filepath):
        mx, my, lbh, rbh = parse_packet(i)
        mouse_emulator.move(mx, my)
        mouse_emulator.set_left_button(lbh)
        mouse_emulator.set_right_button(rbh)
        yield mouse_emulator.snapshot()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", help="Path to the input pcap file.")
    return parser.parse_args()


def main():
    args = parse_args()
    mt = MouseTracer()

    xs = []
    ys = []
    colors = []
    alphas = []
    for snapshot in snapshot_mouse(args.input_file):
        x, y, lbh, rbh = snapshot
        color = "red" if lbh else "grey"
        color = "blue" if rbh else color
        alpha = 1 if lbh or rbh else 0.1
        mt.add(snapshot)
        xs.append(snapshot[0])
        ys.append(snapshot[1])
        colors.append(color)
        alphas.append(alpha)

    plt.scatter(xs, ys, c=colors, alpha=alphas)
    plt.show()


if __name__ == "__main__":
    main()
