"""Hamming(7,4) single-bit error correction."""


def encode(d):
    p1 = d[0] ^ d[1] ^ d[3]
    p2 = d[0] ^ d[2] ^ d[3]
    p3 = d[1] ^ d[2] ^ d[3]
    return [p1, p2, d[0], p3, d[1], d[2], d[3]]


def decode(c):
    s1 = c[0] ^ c[2] ^ c[4] ^ c[6]
    s2 = c[1] ^ c[2] ^ c[5] ^ c[6]
    s3 = c[3] ^ c[4] ^ c[5] ^ c[6]

    pos = s1 + 2 * s2 + 4 * s3

    corrected = c[:]
    if pos != 0:
        corrected[pos - 1] ^= 1

    data = [corrected[2], corrected[4], corrected[5], corrected[6]]
    return pos, data, corrected


word = encode([1, 0, 1, 1])
print("codeword        :", "".join(map(str, word)))

for flip in (None, 5):
    received = word[:]
    if flip:
        received[flip - 1] ^= 1
    position, data, corrected = decode(received)
    print(f"error at {str(flip):<4}: syndrome {position}, "
          f"data {''.join(map(str, data))}")

# Demonstrate a two-bit error: standard Hamming(7,4) cannot reliably
# correct two-bit errors; the syndrome may point to an incorrect bit.
received_two_errors = word[:]
received_two_errors[1] ^= 1
received_two_errors[4] ^= 1
position, data, corrected = decode(received_two_errors)
print("two-bit error received:", "".join(map(str, received_two_errors)))
print("two-bit syndrome:", position)
print("decoder output data:", "".join(map(str, data)))
