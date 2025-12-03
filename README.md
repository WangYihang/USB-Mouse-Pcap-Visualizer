## Description

A forensic script that can help you to extract mouse movement / click data from usb traffic files.

![Animation](https://github.com/WangYihang/USB-Mouse-Pcap-Visualizer/assets/16917636/1dd15ae6-ef58-416d-b5af-8cd8aaceeaaf)

## Installation

### Clone this repository

```bash
git clone https://github.com/WangYihang/USB-Mouse-Pcap-Visualizer.git
```

### Install Python dependencies

```bash
cd USB-Mouse-Pcap-Visualizer
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh
# Install dependencies
uv sync
```

### Install tshark

> Winodws

Install WireShark and add `tshark` to your `PATH`.

> Linux (Ubuntu)

```bash
sudo apt install tshark
```

## Usage

```bash
$ uv run python usb-mouse-pcap-visualizer.py --help
Usage: usb-mouse-pcap-visualizer.py [OPTIONS]

Options:
  -i, --input-file TEXT  Path to the input pcap file.  [required]
  -o, --output-file TEXT
                          Path to the output csv file.  [required]
  --help                 Show this message and exit.
```

```bash
uv run python usb-mouse-pcap-visualizer.py -i assets/example/XNUCA/data.pcap -o assets/example/XNUCA/data.csv
```

The csv file can be visualized by `assets/index.html`, or try it [online](https://usb-mouse-pcap-visualizer.vercel.app/).

```csv
timestamp,x,y,left_button_holding,right_button_holding
1478943238.284336,0,0,False,False
1478943238.899621,0,0,False,False
1478943238.899621,0,0,False,False
```

![](assets/example/XNUCA/data.png)


## Demonstration Videos

* https://www.youtube.com/watch?v=unBwmcpXbhE
