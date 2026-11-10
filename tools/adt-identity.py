#!/usr/bin/env python3
"""adt-identity.py IN OUT  -- add the factory identity MobileGestalt needs for the UDID.

MobileGestalt builds UniqueDeviceID on A11 phones from the serial number, the ECID and the Wi-Fi and
Bluetooth addresses. With one missing it asks MobileGestaltHelper for the factory data, is refused,
and waits forever; on a fresh /var lsd waits with it while seeding (GenerateBuiltInAppInstallSessionID)
and SpringBoard waits on lsd. Same properties as HackiOS's loader; synthetic values (locally
administered MACs, made-up serials), not the phone's.
"""
import struct, sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
import adt

ROOT = [
    ('serial-number', b'SHMRK0000001'),
    ('mlb-serial-number', b'SHMRK0000001MLB01'),
    ('model-number', b'MQ8D2'),
    ('region-info', b'LL/A'),
    ('regulatory-model-number', b'A1897'),
]
CHOSEN = [
    ('mac-address-wifi0', bytes([0x02, 0x53, 0x48, 0x4d, 0x00, 0x01])),
    ('mac-address-bluetooth0', bytes([0x02, 0x53, 0x48, 0x4d, 0x00, 0x02])),
    ('board-id', struct.pack('<I', 0x0e)),
]


def put(node, name, val):
    for i, (n, f, v) in enumerate(node.props):
        if n == name:
            node.props[i] = (n, f, val)
            return 'replaced'
    node.props.append((name, 0, val))
    return 'added'


buf = adt.load(sys.argv[1])
root, _ = adt.parse(buf)
for name, val in ROOT:
    print('/', name, put(root, name, val.ljust(32, b'\0')))
chosen = [c for c in root.children if c.name == 'chosen'][0]
for name, val in CHOSEN:
    print('/chosen', name, put(chosen, name, val))
open(sys.argv[2], 'wb').write(adt.serialize(root))
