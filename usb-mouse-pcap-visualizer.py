#!/usr/bin/env python
import csv
import enum
import json
import struct

import pyshark
import structlog
import tqdm
import typer

logger = structlog.get_logger()


class Opcode(enum.Enum):
    LEFT_BUTTON_HOLDING = 0b00000001
    RIGHT_BUTTON_HOLDING = 0b00000010


class MouseSnapshot():
    def __init__(self, timestamp: float, x: int, y: int, left_button_holding: bool, right_button_holding: bool):
        self.timestamp = timestamp
        self.x = x
        self.y = y
        self.left_button_holding = left_button_holding
        self.right_button_holding = right_button_holding

    def __repr__(self):
        return f"MouseSnapshot(timestamp={self.timestamp}, x={self.x}, y={self.y}, left_button_holding={self.left_button_holding}, right_button_holding={self.right_button_holding})"


class MouseSnapshotEncoder(json.JSONEncoder):
    def default(self, obj: object | None):
        if isinstance(obj, MouseSnapshot):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class MouseEmulator:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.left_button_holding = False
        self.right_button_holding = False

    def move(self, x: int, y: int):
        self.x += x
        self.y -= y

    def set_left_button(self, state: bool):
        self.left_button_holding = state

    def set_right_button(self, state: bool):
        self.right_button_holding = state

    def snapshot(self, timestamp: float):
        return MouseSnapshot(timestamp=timestamp, x=self.x, y=self.y, left_button_holding=self.left_button_holding, right_button_holding=self.right_button_holding)


class MouseTracer:
    def __init__(self):
        self.snapshots: list[MouseSnapshot] = []

    def add(self, snapshot: MouseSnapshot):
        self.snapshots.append(snapshot)

    def save(self, path: str):
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                ['timestamp', 'x', 'y', 'left_button_holding', 'right_button_holding'],
            )
            for snapshot in self.snapshots:
                writer.writerow([
                    snapshot.timestamp, snapshot.x, snapshot.y,
                    snapshot.left_button_holding, snapshot.right_button_holding,
                ])


def load_pcap(filepath: str):
    cap = pyshark.FileCapture(filepath)
    for packet in tqdm.tqdm(cap):
        if hasattr(packet, 'DATA'):
            usbhid_data = packet.DATA.get_field('usbhid_data')
            usb_capdata = packet.DATA.get_field('usb_capdata')
            timestamp = float(packet.sniff_timestamp)
            for data in [usbhid_data, usb_capdata]:
                if data:
                    yield (timestamp, data)


def parse_packet(payload: str):
    items = [
        struct.unpack('b', bytes.fromhex(i))[0]
        for i in payload.split(':')
    ]

    state, movement_x, movement_y = 0, 0, 0

    if len(items) == 4:
        state, movement_x, movement_y, _ = items

    if len(items) == 8:
        state, _, movement_x, _, movement_y, _, _, _ = items

    left_button_holding = state & Opcode.LEFT_BUTTON_HOLDING.value != 0
    right_button_holding = state & Opcode.RIGHT_BUTTON_HOLDING.value != 0

    return movement_x, movement_y, left_button_holding, right_button_holding


def snapshot_mouse(filepath: str):
    mouse_emulator = MouseEmulator()
    for timestamp, data in load_pcap(filepath):
        mx, my, lbh, rbh = parse_packet(data)
        mouse_emulator.move(mx, my)
        mouse_emulator.set_left_button(lbh)
        mouse_emulator.set_right_button(rbh)
        yield mouse_emulator.snapshot(timestamp)


app = typer.Typer()


@app.command()
def main(
    input_file: str = typer.Option(
        ..., '-i', '--input-file',
        help='Path to the input pcap file.',
    ),
    output_file: str = typer.Option(
        ..., '-o', '--output-file',
        help='Path to the output csv file.',
    ),
):
    logger.info(
        'Starting processing', input_file=input_file,
        output_file=output_file,
    )
    mt = MouseTracer()
    for snapshot in snapshot_mouse(input_file):
        mt.add(snapshot)
    logger.info('Snapshots loaded', count=len(mt.snapshots))
    mt.save(output_file)
    logger.info('Mouse snapshots saved', output_file=output_file)
    logger.info(
        'Visualization ready',
        message='visualize the data by opening the assets/index.html file in your browser.',
    )


if __name__ == '__main__':
    app()
