"""
Animacy

Linear buffer tests.

Copyright (c) 2026 Sparky Bobo
"""

from animacy.utils.linear_buffer import (
    LinearBuffer,
    LinearBufferReader,
    LinearBufferWriter,
)


def test_buffer_init():
    buffer = LinearBuffer()
    reader:LinearBufferReader = buffer
    assert not reader.peek(0)
    assert reader.available() == 0
    assert buffer.head == 0
    assert buffer.tail == 0

def test_buffer_reset():
    buffer = LinearBuffer()
    reader:LinearBufferReader = buffer
    writer:LinearBufferWriter = buffer
    writer.append([0x1,0x2,0x3])
    assert buffer.head == 0
    assert buffer.tail == 3

    writer.reset()
    assert not reader.peek(0)
    assert reader.available() == 0
    assert buffer.head == 0
    assert buffer.tail == 0

def test_buffer_append_bytearray():
    buffer = LinearBuffer()
    reader:LinearBufferReader = buffer
    writer:LinearBufferWriter = buffer
    writer.append(bytearray([0x1,0x2,0x3]))
    assert buffer.head == 0
    assert buffer.tail == 3
    assert reader.available() == 3
    assert reader.peek(0)[0] == 0x1
    assert reader.peek(1)[0] == 0x2
    assert reader.peek(2)[0] == 0x3

def test_buffer_append_bytes():
    buffer = LinearBuffer()
    reader:LinearBufferReader = buffer
    writer:LinearBufferWriter = buffer
    writer.append(bytes([0x1,0x2,0x3]))
    assert buffer.head == 0
    assert buffer.tail == 3
    assert reader.available() == 3
    assert reader.peek(0)[0] == 0x1
    assert reader.peek(1)[0] == 0x2
    assert reader.peek(2)[0] == 0x3

def test_buffer_append_multiple():
    buffer = LinearBuffer()
    reader:LinearBufferReader = buffer
    writer:LinearBufferWriter = buffer
    writer.append(bytes([0x1,0x2,0x3]))
    writer.append(bytes([0x4,0x5,0x6]))
    writer.append(bytes([0x7,0x8,0x9]))
    assert buffer.head == 0
    assert buffer.tail == 9
    assert reader.available() == 9
    assert reader.peek(0)[0] == 0x1
    assert reader.peek(1)[0] == 0x2
    assert reader.peek(2)[0] == 0x3
    assert reader.peek(6)[0] == 0x7
    assert reader.peek(7)[0] == 0x8
    assert reader.peek(8)[0] == 0x9

def test_buffer_consume():
    buffer = LinearBuffer()
    reader:LinearBufferReader = buffer
    writer:LinearBufferWriter = buffer
    writer.append((0x1,0x2,0x3))
    writer.consume(1)
    assert buffer.head == 1
    assert buffer.tail == 3
    assert reader.available() == 2
    assert reader.peek(0)[0] == 2

def test_buffer_consume_all():
    buffer = LinearBuffer()
    reader:LinearBufferReader = buffer
    writer:LinearBufferWriter = buffer
    writer.append((0x1,0x2,0x3))
    writer.consume(3)
    assert buffer.head == 0
    assert buffer.tail == 0
    assert reader.available() == 0
    assert reader.peek(0) != 0
