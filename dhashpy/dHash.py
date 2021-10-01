"""

    Introduction
    =============
    The `dhashpy <https://github.com/akamhy/dhashpy>`_ implements the row-wise
    gradient dHash (difference hash) algorithm.

    dHash algorithm was originally described at `Kind of Like That  - The Hacker Factor Blog
    <https://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html>`_

    The dHash algorithm works by converting the input image to grayscale,
    shrinking it to a smaller size and then leveraging the fact that for the
    grayscale images, the pixel value is just a single number that represents
    the brightness of the pixel. And measuring the difference in brightness
    between the adjacent pixels to generate the hash value for the input image.

    The difference between the brightness of the grayscaled image can be
    calculated either row-wise(along the row) or column-wise(along the columns).
    This identifies the relative brightness gradient direction for the rows or
    the columns respectively.

    The dhashpy package implements the row-wise difference based dHash algorithm
    and therefore calculates difference between in brightness the adjacent
    pixels in a row and not in a column.


    The dHash algorithm in dhashpy
    ==============================

    The exact implementation of the row-wise difference dHash algorithm in
    dhashpy package is explained below. And can be used to calculate the exact
    same hash output if you want to implement it in an another language.

    - Convert the input image to grayscale using the ITU-R 601-2 luma transform.

      **L = R * 299/1000 + G * 587/1000 + B * 114/1000**

      Every pixel is now just an integer, a shade of grey from the possible 256
      shades of grey.

    - Remove the high frequencies and detail by shrinking(resize) the image.
      The default setting is to resize every image to 9x8 pixels(width, height).
      As this implementation takes row wise difference, we need to shrink the
      image to **(n+1)x(n)**. The width is bigger by one pixel. There are now
      total (n^2 + n) pixels/shade of grey in the image.

    - Now compare the adjacent pixels along a row. And if the pixel on the right
      side of the current pixel is more bright than the current pixel set the bit
      value to 0 else set the value to 1. As there are (n+1) pixel is a row thus
      there will be n number of differences. Total number of differences for all
      the n rows will be (n^2)bits.

    - Join the values from left to right and top to bottom to form a binary
      string. Don't forget to prefix the string with "0b", indicating that it's
      a binary string. The length of this binary string should be (n^2 + 2),
      (n^2) number of bit and 2 for the prefix "0b".

    - As the string is a binary string and too long, it's better to store the
      hexadecimal value of this binary string if storage is an issue.
      But if storing large strings is not an issue it's better to store the
      binary string as storing the binary strings will reduce the compute cost
      of converting the hexadecimal strings to binary every time we want to
      compare the hash values. The comparisons must be done on the original
      binary string and never on the hexadecimal representation of the strings.
      Hexadecimal strings should be prefixed with "0x" indicating that they are
      hexadecimal representation of the hash value.

    - Hamming distance is used to calculate the difference between the hash
      values(the binary strings). The result of the hamming distance of the
      two binary strings is the relative difference between the two images.
      Hamming distance for strings of unequal length is not defined.

    Example, when n=8, the default value:
    =====================================

        - If n = 8, height is 8 pixels. The width(n+1) should be 8+1 = 9 pixels.

        The following structure is a 9x8 pixel distribution::

            |----------------- WIDTH ----------------------->
            H  px1  px2  px3  px4  px5  px6  px7  px8  px9
            E  px10 px11 px12 px13 px14 px15 px16 px17 px18
            I  px19 px20 px21 px22 px23 px24 px25 px26 px27
            G  px28 px29 px30 px31 px32 px33 px34 px35 px36
            H  px37 px38 px39 px40 px41 px42 px43 px44 px45
            T  px46 px47 px48 px49 px50 px51 px52 px53 px54
            |  px55 px56 px57 px58 px59 px60 px61 px62 px63
            |  px64 px65 px66 px67 px68 px69 px70 px71 px72
            V

        - For pixels in a same row let's define a function, value(x) such that:

                **value(x) = 0 for px(x+1) > px(x)**

                **value(x) = 1 for px(x+1) < px(x)**

        .. note::
            We can change the definition of the above function and set value(x) = 1 if
            px(x+1) > px(x) and vice-versa, it's arbitrary but it's very important to be
            consistent.

        - If the next pixel in the same row is a bigger number than the current
          pixel set the value of pixel's position to 0 else 1. For the last
          pixel of each row we don't have the value(x) defined and therefore there
          are n values for (n+1) pixels.

        - For total n number of rows we get (n^2) pixels. Here the number of
          rows is 8 and columns is 9, which is 72 (8*9) pixels and
          64 (8*8) pixel difference values.


        - If px(46+1) > px(46) == px(47) > px(46) then we set the value(46) to 0

        - If px(47) < px(46) than set the value(x) = 1

        - But value(27) is not defined as there is no pixel in the same row to
          compare with.

        - Last pixel of every row is non conformable to the difinition of value(x)
          as last pixels do not have any next pixel in the same row.


    API reference
    =============

"""

from PIL import Image
import os.path


class DHash(object):
    """
    DHash class
    =============
    DHash class provides an interface for computing & comparing dhash values.

    DHash class and it's instance have the following public methods:

    - DHash.hamming_distance(str_a, str_b) : It takes two strings as input for
                                             which the hamming distance will be
                                             returned.

    - DHash.hex2bin(hexstr, padding) : hexstr is the hexadecimal string for
                                       which we want to calculate the binary
                                       value. The binary value is returned as a
                                       string prefixed with "0b", indicating
                                       that the string is binary value.

                                       padding is an integer and is useful when
                                       we compute the hamming distance of the
                                       output. Hamming distance is not defined
                                       for strings of unequal length.


    - DHash.bin2hex(binstr) : Input binary string is converted to output
                              hexadecimal value. Both the input binary value and
                              the output hexadecimal value should be prefixed
                              with "0b" and "0x" respectively.


    DHash objects have the following attributes:

    - DHash.path : The path of the input image.

    - DHash.image : Instance of PIL.Image.Image class with the input as the
                    input image.

    - DHash.hash : A binary string prefixed with "0b" is the hash of the input
                   image.

    - DHash.hash_hex : Hexadecimal representation of the binary string hash.

    - DHash.height : The resized height of the input image. Units are pixels.

    - DHash.width : The resized width of the input image. Units are pixels

    - DHash.bits_in_hash : Total number of bits in the hash. Equal n^2, where n
                           is the height.



    """

    def __init__(self, path, height=8):
        """

        Check if path exists.

        :param path: absolute path of the image that needs to be hashed.

        :param height: height must be an integer, it's the height of the scaled
                       image. Units are pixels.
                       If you set height to 4, you will get a
                       4^2 = 16 bits hash value.
                       If you set height to 9 you will get a 81(9^2=81) bits hash.
                       The default value is 8, the default number of bits is 64.
                       The binary string is prefixed with "0b", so a 64 bits hash
                       will have a length of 66(64 hash + 2 for 0b), a 16 bits
                       hash will have a length of 18(16 bit hash and 2 for 0b prefix).

        :return: None

        :rtype: NoneType
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

        self._calc_hash()

    def __str__(self):
        """
        String representation of the instance of DHash class and is same as DHash.hash

        :return: Binary hash value for the image, prefixed with "0b".

        :rtype: str
        """
        return self.hash

    def __len__(self):
        """
        length of the hash, including the prefix 0b. len = bits_in_hash + 2

        :return: Length of the binary hash value for the image.

        :rtype: int
        """
        return len(self.hash)

    def __repr__(self):
        """
        Representation of the instance of DHash class.

        :return: String representation of the object of DHash class.

        :rtype: str
        """
        return "DHash(hash=%s, hash_hex=%s, path=%s)" % (
            self.hash,
            self.hash_hex,
            self.path,
        )

    def __ne__(self, other):
        """
        Implement '!=' on the instance of DHash class.

        :param other: Can be instance of DHash class or a string starting
                      with "0x" or "0b", representing hexadecimal or binary
                      value.

        :return: Return True if not equal else return False.

        :rtype: bool
        """
        if self.__eq__(other):
            return False
        return True

    def __eq__(self, other):
        """
        Implement '==' on the instance of DHash class.

        :param other: Can be instance of DHash class or a string starting
                      with "0x" or "0b", representing hexadecimal or binary
                      value.

        :return: Return True if equal else return False.

        :rtype: bool
        """

        if self.__sub__(other) == 0:
            return True
        return False

    def __sub__(self, other):
        """
        Implement the usage of '-' on instance of DHash class and
        Also compatibile with hexadecimal and binary strings

        :param other: Can be instance of DHash class or a string starting
                      with "0x" or "0b", representing hexadecimal or binary
                      value. If binary string is supplied hash must of the same
                      bits as this instance.

        :return: Hamming distance of the two objects/binary string/hexadecimal
                 string being compared.

        :rtype: int
        """
        if other is None:
            raise TypeError("Other hash is None. And it must not be None.")

        if isinstance(other, str):
            if other.lower().startswith("0x"):
                return DHash.hamming_distance(
                    self.hash, DHash.hex2bin(other.lower(), self.bits_in_hash)
                )
            elif other.lower().startswith("0b"):
                if len(other) != len(self.hash):
                    raise ValueError(
                        "Can not compare different bits hashes. You must supply a %d bits hash."
                        % self.bits_in_hash
                    )
                return DHash.hamming_distance(self.hash, other.lower())
            else:
                raise TypeError(
                    "Hash string must start with either '0x' for hexadecimal or '0b' for binary."
                )

        if isinstance(other, DHash):
            return DHash.hamming_distance(self.hash, other.hash)

        raise TypeError(
            "To calculate difference both of the hashes must be either hexadecimal/binary strings or instance of DHash"
        )

    def _calc_hash(self):
        """
        Open the input image using the pillow package.
        Converts the image to greyscale.
        Resize the image to a smaller pixel value.
        Calculate the binary hash value with the DHash algorithm.


        dHash algorithm as defined at :

        `Kind of Like That  - The Hacker Factor Blog
        <https://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html>`_

        :return: None

        :rtype: NoneType
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
        self.hash_hex = DHash.bin2hex(self.hash)

    @staticmethod
    def hamming_distance(string_a, string_b):
        """
        Computes and returns the hamming distance between the
        two input strings.

        The two input strings must be of equal length as the Hamming distance is
        undefined when strings are of unequal length.

        :param string_a: A python string representing a binary number, prefixed with "0b"

        :param string_b: A python string representing a binary number, prefixed with "0b"

        :return: Hamming distance between the two input strings.

        :rtype: int

        :raises ValueError: When both the strings are not of equal length.
        """
        if len(string_a) != len(string_b):
            raise ValueError(
                "Strings are of unequal length can not compute hamming distance. Hamming distance is undefined."
            )
        return sum(char_1 != char_2 for char_1, char_2 in zip(string_a, string_b))

    @staticmethod
    def hex2bin(hexstr, padding):
        """
        Convert the input string from hexadecimal to binary representation.


        :param hexstr: hexadecimal string and must be prefixed with "0x".

        :param padding: integer indicating the required padding for the string.
                        padding is useful if hamming distance of the output
                        binary string is to be computed. Hamming distance is not
                        defined for strings of unequal length.

        :return: Binary representation of the input hexadecimal string.

        :rtype: str

        :raises ValueError: If hexadecimal input string is not prefixed with "0x".
        """
        if not hexstr.lower().startswith("0x"):
            raise ValueError("Input hexadecimal string must have '0x' as the prefix.")
        return "0b" + str(bin(int(hexstr.lower(), 0))).replace("0b", "").zfill(padding)

    @staticmethod
    def bin2hex(binstr):
        """
        Converts input string from Binary to hexadecimal representation.

        :param binstr: Binary string and must be prefixed with "0b".

        :return: Hexadecimal representation of the input
                 binary string prefixed with "0x" indicating that it's
                 hexadecimal string.

        :rtype: str

        :raises ValueError: If binary input string is not prefixed with "0b".
        """
        if not binstr.lower().startswith("0b"):
            raise ValueError("Binary string must be prefixed with '0b'.")
        return str(hex(int(binstr, 2)))
