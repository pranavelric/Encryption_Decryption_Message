from constants import constants


class Encryption(object):

    sBox = constants().getSBox()
    sBoxInv = constants().getSBoxInv()

    # Defining Round Keys for: Pre round transformation K0 = w0+w1; K1= w2+w3; K2=w4+w5;
    def __init__(self, keys):
        self.pre_round_transformation_key, self.round1_key, self.round2_key = self.keyExpansion(
            keys)

    # Creates three 16-bit round keys from one single 16-bit cipher key

    def keyExpansion(self, keys):
        # Round constants
        rCon1 = 0x80
        rCon2 = 0x30

        # Calculate value of each word
        w = [None]*6
        w[0] = (keys & 0xFF00) >> 8
        w[1] = keys & 0x00FF

        # Each nibble in the word is  substituted by  another nibble using the Sbox table
        w[2] = w[0] ^ (((self.sBox[((((w[1] & 0x0F) << 4) + ((w[1] & 0xF0) >> 4)) >> 4)] <<
                         4) + self.sBox[(((w[1] & 0x0F) << 4) + ((w[1] & 0xF0) >> 4)) & 0x0F]) ^ rCon1)
        w[3] = w[2] ^ w[1]
        w[4] = w[2] ^ (((self.sBox[((((w[3] & 0x0F) << 4) + ((w[3] & 0xF0) >> 4)) >> 4)] <<
                         4) + self.sBox[(((w[3] & 0x0F) << 4) + ((w[3] & 0xF0) >> 4)) & 0x0F]) ^ rCon2)
        w[5] = w[4] ^ w[3]

        return (
            # Pre-Round-transfromation key
            self.intToState((w[0] << 8) + w[1]),
            # Round 1 key
            self.intToState((w[2] << 8) + w[3]),
            # Round 2 key
            self.intToState((w[4] << 8) + w[5]),
        )

    # Galois field multiplication of first and second number  in GF(2^4) / x^4 + x + 1
    def galoisFieldMultiplication(self, first, second):
        product = 0
        first = first & 0x0F
        second = second & 0x0F

        # while both numbers are non-zero
        while first and second:

            # If Least Significant Bit of second is 1
            if second & 1:
                # Add current first number to product
                product = product ^ first

            # Update first  to first * 2
            first = first << 1

            # If a overflows beyond 4th bit
            if first & (1 << 4):

                # XOR with irreducible polynomial with high term eliminated
                first = first ^ 0b10011

            # Update second to second // 2
            second = second >> 1

        return product

    # Convert 2-byte integer to 4-element stateMatrix matrix
    def intToState(self, n):
        return [n >> 12 & 0xF, (n >> 4) & 0xF, (n >> 8) & 0xF, n & 0xF]

    # Convert a 4-element stateMatrix matrix into 2-byte integer
    def stateToInt(self, m):
        return (m[0] << 12) + (m[2] << 8) + (m[1] << 4) + m[3]

    # Add round keys in GF
    def addRoundKey(self, first, second):
        a = [i ^ j for i, j in zip(first, second)]
        # print("Add Round Key")
        # print(a)
        return [i ^ j for i, j in zip(first, second)]

    # Nibble substitution using sBox
    def substituteNibbles(self, sbox, stateMatrix):
        sub = [sbox[nibble] for nibble in stateMatrix]
        # print("Substitute nibbles")
        # print(sub)

        return [sbox[nibble] for nibble in stateMatrix]

    # Shifting rows of stateMatrix matrix
    def shiftRows(self, stateMatrix):
        shift = [stateMatrix[0], stateMatrix[1],
                 stateMatrix[3], stateMatrix[2]]
        # print("Shfit Rows")
        # print(shift)

        return [stateMatrix[0], stateMatrix[1], stateMatrix[3], stateMatrix[2]]

    # Mix columns transformation on stateMatrix matrix
    def mixColumns(self, stateMatrix):

        mixCol = [
            stateMatrix[0] ^ self.galoisFieldMultiplication(4, stateMatrix[2]),
            stateMatrix[1] ^ self.galoisFieldMultiplication(4, stateMatrix[3]),
            stateMatrix[2] ^ self.galoisFieldMultiplication(4, stateMatrix[0]),
            stateMatrix[3] ^ self.galoisFieldMultiplication(4, stateMatrix[1]),
        ]
        # print("Mix Columns")
        # print(mixCol)

        return [
            stateMatrix[0] ^ self.galoisFieldMultiplication(4, stateMatrix[2]),
            stateMatrix[1] ^ self.galoisFieldMultiplication(4, stateMatrix[3]),
            stateMatrix[2] ^ self.galoisFieldMultiplication(4, stateMatrix[0]),
            stateMatrix[3] ^ self.galoisFieldMultiplication(4, stateMatrix[1]),
        ]

    # Encrypt plaintext with given key

    def encrypt(self, plaintext):

        # print("Pre Round Transformation")
        # print("\nRound key k0")
        # print(self.pre_round_transformation_key)

        stateMatrix = self.addRoundKey(
            self.pre_round_transformation_key, self.intToState(plaintext))

        stateMatrix = self.mixColumns(self.shiftRows(
            self.substituteNibbles(self.sBox, stateMatrix)))

        # print("\n\nRound 1")
        # print("\nRound key k1")
        # print(self.round1_key)

        stateMatrix = self.addRoundKey(self.round1_key, stateMatrix)

        stateMatrix = self.shiftRows(
            self.substituteNibbles(self.sBox, stateMatrix))

        # print("\n\nRound 2")
        # print("\nRound key k2")
        # print(self.round2_key)

        stateMatrix = self.addRoundKey(self.round2_key, stateMatrix)

        return self.stateToInt(stateMatrix)
