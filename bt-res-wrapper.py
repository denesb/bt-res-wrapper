#!/usr/bin/env python3

import subprocess
import re
import argparse


def resolve_addresses(executable, addresses):
    addr2line = subprocess.Popen(["addr2line", "-Cfpi", "-e", executable], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    addresses_str = '\n'.join(map(lambda a: '0x{0:x}'.format(a), addresses))

    (out, err) = addr2line.communicate(bytes(addresses_str, 'utf-8'))
    addr2line.wait()

    if err:
        return addresses_str
    else:
        return out.decode('utf-8').rstrip()


cmdline_parser = argparse.ArgumentParser(description='Wrap executable and resolve printed backtraces')
cmdline_parser.add_argument('executable', type=str, help='specify the executable to run')

args = cmdline_parser.parse_args()

executable = args.executable

process = subprocess.Popen([executable], bufsize=1, universal_newlines=True, stdout=None, stderr=subprocess.PIPE)

map_re = re.compile("([0-9abcdef]+)-[0-9abcdef]+ r-x. 0+ .*{}".format(executable.split('/')[-1]))

base_addr = 0

with open("/proc/{}/maps".format(process.pid), "r") as map_f:
    for m in map_f:
        match = re.match(map_re, m)
        if match:
            base_addr = int(match.group(1), 16)
            break

print("Process base address is 0x{0:x}".format(base_addr))

address_re = re.compile('\W+(0x[0-9abcdef]+)')
backtrace_mode = False
addresses = []

for line_raw in process.stderr:
    line = line_raw.rstrip()

    if line == "Backtrace:":
        backtrace_mode = True
        addresses = []
        continue

    if not backtrace_mode:
        print(line)
        continue

    match = re.match(address_re, line)
    if match:
        addr = match.group(1)
    else:
        backtrace_mode = False
        print("Backtrace:")
        print(resolve_addresses(executable, addresses))

    addresses.append(int(addr, 16) - base_addr)

process.wait()
