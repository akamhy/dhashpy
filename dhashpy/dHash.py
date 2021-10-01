from PIL import Image
import os.path


class DHash(object):
    """
    The dHash algorithm. It works on the difference between the adjacent pixels.

    We calculate the difference between the adjacent pixels row-wise or column-wise.
    This identifies the relative gradient direction for the row or the column.

    This implementation of dHash calculates difference between the adjacent pixels in a row.

    But first convert the image to grayscale, so that we can compare the pixels.
    Every pixel is now just an integer, a shade of grey from the 256 shades of grey.

    To remove the high frequencies and detail shrink the image.
    As our implementation takes row wise difference, we need to shrink the image to (n+1)x(n)
    the width is bigger by one pixel.

    There are now (n^2 + n) pixels/shade of grey.


    If n = 8, that is height = 8 pixels.
    The width will be 8+1 = 9 pixels.

        | ---------------- WIDTH ----------------------->
        |
        H    px1  px2  px3  px4  px5  px6  px7  px8  px9
        E    px10 px11 px12 px13 px14 px15 px16 px17 px18
        I    px19 px20 px21 px22 px23 px24 px25 px26 px27
        G    px28 px29 px30 px31 px32 px33 px34 px35 px36
        H    px37 px38 px39 px40 px41 px42 px43 px44 px45
        T    px46 px47 px48 px49 px50 px51 px52 px53 px54
        |    px55 px56 px57 px58 px59 px60 px61 px62 px63
        V    px64 px65 px66 px67 px68 px69 px70 px71 px72

    diff(x) = px(x+1) - px(x) if px(x+1)'s row is same as that of p(x).


    If diff(x) > 0:
        value(x) = 0 # the x'th pixel is smaller integer compared to it's next one in the same row.
    else:
        value(x) = 1 # if x't pixel is larger than it's next one in the same row.

    # We can change the above and set value(x) = 1 if diff(x) > 0, it's arbitrary but stay consistent.

    Example:
    diff(46) = px(46+1) - px(46) = px(47) - px(46)
    If diff(46) > 0 we set the value(x) = 0
    If diff(46) < 0 we set the value(x) = 1

    But diff(27) is not defined as the next pixel is on the next row.

    We can clearly see that the last pixel of every row is non conformable to the diff(x) as it
    does not have any next pixel in the same row.

    For each row we will get 8 bits and there are 8 rows.
    Which becomes 64 bits.

    If height is n then number of bits will be n^2.
    """

    def __init__(self, path, height=8):
        """

        Check if path exists.

        :param path: absolute path of the image that needs to be hashed.

        :param height: height must be an integer, it's the height of the scaled
                       image. Units are pixels.
                       If you set height to 4, you will get a
                       4**2 = 16 bits hash.
                       If you set height to 9 you will get a 81(9^2=81) bits hash.
                       The default value is 8, the default number of bits is 64.
                       The binary string is prefixed with "0b", so a 64 bits hash
                       will have a length of 66(64 hash + 2 for 0b), a 16 bits
                       hash will have a length of 18(16 bit hash and 2 for 0b prefix).
        """
        self.path = path
        self.image = None
        self.hash = None
        self.hash_hex = None
        self.height = height
        self.bits_in_hash = self.height * self.height
        self.width = self.height + 1

        if not os.path.isfile(self.path):
            raise FileNotFoundError("No image file found at '%s'." % self.path)

        self.calc_hash()

    def __str__(self):
        """String representation of the instance of DHash class and is same as DHash.hash"""
        return self.hash

    def __len__(self):
        """length of the hash, including the prefix 0b. len = bits_in_hash + 2"""
        return len(self.hash)

    def __repr__(self):
        """Representation of the instance of DHash class."""
        return "DHash(hash=%s, hash_hex=%s, path=%s)" % (
            self.hash,
            self.hash_hex,
            self.path,
        )

    def __eq__(self, other):
        """
        Implement '==' on the instance of DHash class.

        :param other: Can be instance of DHash class or a string starting
                      with "0x" or "0b", representing hexadecimal or binary
                      value.
        """

        if self.__sub__(other) == 0:
            return True
        return False

    def __ne__(self, other):
        """
        Implement '!=' on the instance of DHash class.

        :param other: Can be instance of DHash class or a string starting
                      with "0x" or "0b", representing hexadecimal or binary
                      value.
        """
        if self.__eq__(other):
            return False
        return True

    def __sub__(self, other):
        """
        Implement the usage of '-' on instance of DHash class and
        Also compatibile with hexadecimal and binary strings

        :param other: Can be instance of DHash class or a string starting
                      with "0x" or "0b", representing hexadecimal or binary
                      value. If binary string is supplied hash must of the same
                      bits as this instance.
        """
        if other is None:
            raise TypeError("Other hash is None. And it must not be None." % other)

        if isinstance(other, str):
            if other.lower().startswith("0x"):
                return self.hamming_distance(self.hash, self.hex2bin(other.lower()))
            elif other.lower().startswith("0b"):
                if len(other) != len(self.hash):
                    raise ValueError(
                        "Can not compare different bits hashes. You must supply a %d bits hash."
                        % self.bits_in_hash
                    )
                return self.hamming_distance(self.hash, other.lower())
            else:
                raise TypeError(
                    "Hash string must start with either '0x' for hexadecimal or '0b' for binary."
                )

        if isinstance(other, DHash):
            return self.hamming_distance(self.hash, other.hash)

        raise TypeError(
            "To calculate difference both of the hashes must be either hexadecimal/binary strings or instance of DHash"
        )

    def hamming_distance(self, string_a, string_b):
        """
        Calculate hamming distance between two strings.

        :param string_a: Binary string
        :param string_b: Binary string
        """
        return sum(char_1 != char_2 for char_1, char_2 in zip(string_a, string_b))

    def hex2bin(self, hexstr):
        """
        Convert string from hexadecimal to binary
        make sure that the binary string length is always
        64 bits padded with 0b.

        :param hexstr: hexadecimal string must start with "0x"
        """
        return "0b" + str(bin(int(hexstr, 0))).replace("0b", "").zfill(
            self.bits_in_hash
        )

    def bin2hex(self, binstr):
        """
        Convert string from Binary to hexadecimal.

        :param binstr: Binary string must start with "0b"
        """
        return str(hex(int(binstr, 2)))

    def calc_hash(self):
        """
        Implementation based on:
        https://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html

        """
        self.image = Image.open(self.path)
        self.image = self.image.convert("L")
        self.image = self.image.resize((self.width, self.height), Image.ANTIALIAS)
        lpixels = list(self.image.getdata())
        self.hash = "0b"
        for i, pixel in enumerate(lpixels):
            if (i + 1) % self.width == 0 and i != 0:
                continue
            if pixel < lpixels[i + 1]:
                self.hash += "1"
                continue
            self.hash += "0"
        self.hash_hex = self.bin2hex(self.hash)
