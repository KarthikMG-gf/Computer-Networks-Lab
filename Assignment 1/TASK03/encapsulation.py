"""Layer-by-layer encapsulation and decapsulation demonstration."""

LAYERS = [
    ("Application", "HTTP"),
    ("Transport", "TCP"),
    ("Network", "IP"),
    ("Data link", "ETH")
]


def send(message):
    pdu = message
    for layer, tag in LAYERS:
        if tag == "ETH":
            pdu = f"[{tag}|{pdu}|FCS]"
        else:
            pdu = f"[{tag}|{pdu}]"
        print(f"{layer:<12} adds {tag:<4} -> {len(pdu)} bytes")
    return pdu


def receive(frame):
    pdu = frame
    for layer, tag in reversed(LAYERS):
        head = "[" + tag + "|"
        tail = "|FCS]" if tag == "ETH" else "]"
        assert pdu.startswith(head) and pdu.endswith(tail), f"{layer}: bad header"
        pdu = pdu[len(head):-len(tail)]
    return pdu


frame = send("GET /results")
print("on the wire:", frame)
print("delivered :", receive(frame))
print(f"overhead : {len(frame) - len('GET /results')} bytes for 12 bytes of data")

# Additional comparison: a 1,400-character payload using this illustrative
# string-header model. Real Ethernet/IP/TCP overhead is calculated separately
# in the written analysis, not by counting these demonstration tags.
large_message = "A" * 1400
large_frame = send(large_message)
print("1400-byte payload model overhead:", len(large_frame) - len(large_message), "bytes")
print("1400-byte payload model overhead percentage:",
      (len(large_frame) - len(large_message)) / len(large_frame) * 100, "%")
