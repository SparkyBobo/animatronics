# MIDI File Transfers

## Overview

The DaBones use MIDI System Exclusive messages to transfer files to all show elements. System Exclusive
messages have the form:

Byte|Meaning
---|-------
11110000
0iiiiiii|(iiiiiii) is usually a seven-bit Manufacturer's I.D. code. Always 7Eh followed by the MIDI channel number.
0ddddddd|data byte 0
..|data byte(s)
0ddddddd|data byte n
11110111|end of message

## Manufacturers I.D. Code

The universal system exclusive messages provide plenty of functionality to support file transfers. Therefore, the
manufacturer ID code will always be 7Eh followed by the MIDI channel number, e.g., 01111110 0000cccc. If channel
0 is used, all devices will receive the file.

## Messages

The universal system exclusive messages define sub IDs 1 and 2 to define messages. The following messages are supported for file transfers using the open loop protocol:

Sub ID1|Sub ID2|Data|Comment
-------|-------|----|-------
07|01|'MIDI' 0lllllll 0lllllll 0lllllll 0lllllll 'name'|File Header
07|02|0ppppppp 0lllllll ....|File Data
7B|||End of File

### File Header

The file header command `07 01` is followed by the file type in ASCII, 'MIDI', the file length as 4 7-bit bytes LSB first, and finally the name of the file in ASCII.

The file length is the raw file length, not the length of the encoding.

### File Data

The file data command `07 02` is followed by a packet number 0ppppppp, the number of encoded data bytes minus one, i.e. 0=one byte, 7F=128 bytes, and finally the file data encoded as 7 file bytes for every 8 received bytes, followed by the 7-bit XOR of all data bytes following the SOX `F0` including `7E` and the address up to the checksum byte.

The packet count is a 7-bit value (0-127) which wraps around from 127 to 0 as necessary.

Each set of 7 file-bytes (represented in binary here) with the Most Significant Bits stripped off and sent separately, packed into the first byte.

File data (8-bit)|->|encoded MIDI data-bytes (7-bit)
-----------------|--|------------------------------
Aaaaaaaa||0ABCDEFG
Bbbbbbbb||0aaaaaaa
Cccccccc||0bbbbbbb
Dddddddd||0ccccccc
0ddddddd|->|
Eeeeeeee||0eeeeeee
Ffffffff||0fffffff
Gggggggg||0ggggggg

In the case where there are less than 7 bytes to be encoded, the unused bits of the first byte are set to zero:

File data (8-bit)|->|encoded MIDI data-bytes (7-bit)
-----------------|--|------------------------------
Aaaaaaaa||0AB00000
Bbbbbbbb|->|
0bbbbbbb||0aaaaaaa

### End of File (EOF)
This message signifies that the end of the file has been reached and that the data transfer has been completed successfully.

## Transfer Procedure

### Sender

To initiate a file transfer, a File Header message is sent. The header includes the file length and name.

Due to the MIDI hardware involved, an open-loop (no handshaking) protocol is used. The sender starts the transfer
after sending the File Header message and sends the next data packet. This process continues until there are less than 121 data bytes remaining to be sent. The final packet will still consist of 120 bytes, regardless of the actual remaining bytes, with the excess bytes all being 0.

### Receiver

While receiving a File Header or File Data Packet, a device should keep a running checksum. This calculated checksum can be compared with the checksum within the Data Packet to ascertain whether or not the data was received correctly.

The file data will be buffered and upon completion of the transfer as indicated by an End of File message:

- The length and name are used to write the file after verification
- The checksum for each File Data Packet is correct before buffering the data
- The packet numbers are monotonically increasing and wrap from 127 to 0.
- Once the End of File message is received, the file length is compared with the number of received bytes. If they match, the file is saved using the name from the header.
- If the checksum on a File Data packet or the length from the File Header message do not match the received bytes, the file transfer is aborted and the received contents are discarded.
- Where possible, the receiver will indicate visually whether it has accepted or rejected the file.
