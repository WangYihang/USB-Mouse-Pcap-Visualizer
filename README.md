Description : 
---
```
A forensic tool for extracting mouse movement data from usb traffic packages
and can be drawn as a picture of a mouse
```

Usage : 
---
```
Usage : 
        python UsbMiceHacker.py data.pcap out.png [LEFT|RIGHT|MOVE|ALL]
Tips : 
        To use this python script , you must install the numpy,matplotlib first.
        You can use `sudo pip install matplotlib numpy` to install it.
Author : 
        WangYihang <wangyihanger@gmail.com>
        If you have any questions , please contact me by email.
        Thank you for using.
```

## Demo：

```
1. Step1 , Get data

root@kali:~/桌面/usb/USB/UsbKeyboardDataHacker# tshark -r ./data.pcap -T fields -e usb.capdata
00:00:09:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:0f:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:04:00:00:00:00:00
00:00:00:00:00:00:00:00
00:00:0a:00:00:00:00:00
00:00:00:00:00:00:00:00
20:00:00:00:00:00:00:00
20:00:2f:00:00:00:00:00
...


2. Step2 , decode

root@kali:~/桌面/usb/USB/UsbKeyboardDataHacker# python UsbMiceDataHacker.py ./example.pcap 
[-] Unknow Key : 01
[-] Unknow Key : 01
[+] Found : flag{pr355_0nwards_a2fee6e0}
```

Example video:
---

```
https://www.youtube.com/watch?v=unBwmcpXbhE
```

## Cryptanalysis of the Autokey Cipher

### Demo :

```shell
root@kali:~/桌面/usb# python break_autokey.py 
-824.697138698 autokey, klen 3 :"YCI", ONDDICCUXCERSFORFKKSWPDHRNTDERUVXRPRUGCAZZLSOYMESWPEESTJAPAXANPPYDSEGJPSYKMCBCEUGWGCWMNPTUWMYATGHQHVBPMSTBATZMIWSPTHTG
-772.470967688 autokey, klen 4 :"SYNR", URYABOHCYQRMWTOXOFNASUIDOWSRDOFILXFGAYOOFDXDIGHPICMHSFLGADYRPKOYWITENTAUUGEGRICPRSYTBARSEHUNOPLRTUCLYCFIKLNEQBOROWBIUD
-803.48764464 autokey, klen 5 :"BCGKY", LNFHXUSXSHEWXRYFOBKZBLUTHPPAYDIKONHGBHGNZAELAKEOFIJSMCPEAWHILNQIDHUMBYMEVYGOHTIPUTHADYWEFENJORBRYVWBAYMXHNUADFOBEUKLHV
-761.616653993 autokey, klen 6 :"KIDAHF", CHIROADVRNKOROOWAKKJSDVTWHIRWRBSGUOXKDNAREBOAJNOPUTNNTITZVWEHUNUPOAIWHEKHRITHEZEAHTETOPEMDSRDSTBPSKKYVSBYDURILDSKGHOFH
-743.720273262 autokey, klen 7 :"KIDEAFY", CHINVAHASWLTUCFRONIDEUEPTIXQXGIGGOURFNNORHUMAWQBJOHWERWEEBNTYRILKFOESTIOCLAISGSTXASQMAWOFPVTSARZSOUKRFIBUTIVVEABLPUEEZ
-674.914569565 autokey, klen 8 :"FLAGHERE", HELLOBOYSANDGIRLSYOUARESOSMARTTHATYOUCANFINDTHEFLAGTHATIHIDEINTHEKEYBOARDPACKAGEFLAGISJHAWLZKEWXHNCDHSLWBAQJTUQZDXZQPF
```

