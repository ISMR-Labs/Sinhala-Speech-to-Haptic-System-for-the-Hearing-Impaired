"""Transports to the vest: HTTP over Wi-Fi, USB serial, or an on-screen simulator."""

import sys
import time


class HttpVest:
    def __init__(self, host="vest.local", timeout=2.0):
        import requests  # local import so the simulator works without it
        self.requests = requests
        self.base = host if host.startswith("http") else f"http://{host}"
        self.timeout = timeout

    def send(self, wire):
        r = self.requests.post(self.base + "/play", data=wire.encode(), timeout=self.timeout)
        r.raise_for_status()
        return r.text

    def stop(self):
        return self.requests.post(self.base + "/stop", timeout=self.timeout).text

    def status(self):
        return self.requests.get(self.base + "/status", timeout=self.timeout).text


class SerialVest:
    def __init__(self, port, baud=115200):
        import serial
        # do not toggle DTR/RTS: it resets the ESP32
        self.ser = serial.Serial()
        self.ser.port, self.ser.baudrate, self.ser.timeout = port, baud, 1
        self.ser.dtr = False
        self.ser.rts = False
        self.ser.open()
        time.sleep(0.2)

    def send(self, wire):
        self.ser.write((wire + "\n").encode())
        return self.ser.readline().decode(errors="ignore").strip()

    def stop(self):
        return self.send("S")

    def status(self):
        return self.send("?")


class SimVest:
    """Prints each frame as two 3x3 grids and sleeps for its duration, so a sentence 'plays'."""

    def __init__(self, out=sys.stdout, realtime=True):
        self.out, self.realtime = out, realtime

    def _grid(self, on, side):
        rows = []
        for r in range(3):
            rows.append(" ".join("#" if (side + r * 3 + c) in on else "." for c in range(3)))
        return rows

    def send(self, wire):
        gap = 80
        for part in wire.split(";"):
            part = part.strip()
            if not part:
                continue
            if part[0] == "G":
                gap = int(part[1:])
                continue
            idxs, ms, level = part[1:].split()
            on = {int(i) for i in idxs.split(",")}
            f, b = self._grid(on, 0), self._grid(on, 9)
            self.out.write(f"   front   back    {ms} ms  level {level}\n")
            for i in range(3):
                self.out.write(f"   {f[i]}   {b[i]}\n")
            self.out.flush()
            if self.realtime:
                time.sleep((int(ms) + gap) / 1000)
        return "OK (sim)"

    def stop(self):
        return "OK (sim)"

    def status(self):
        return "simulator"


def open_vest(target):
    """target: 'sim', a serial port path, or a host/URL."""
    if target == "sim":
        return SimVest()
    if target.startswith("/dev/") or target.upper().startswith("COM"):
        return SerialVest(target)
    return HttpVest(target)
