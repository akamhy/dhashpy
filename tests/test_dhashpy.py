import pytest
import os
from dhashpy import DHash
import urllib.request


this_dir = os.path.dirname(os.path.realpath(__file__))


def test_all():
    # Image Attribution: © Sergey Pesterev / Wikimedia Commons / CC BY-SA 4.0
    # https://commons.wikimedia.org/wiki/File:Baikal_ice_on_sunset.jpg
    big_baikal_filename = os.path.join(this_dir, "baikal_big.jpeg")
    big_baikal_url = (
        "https://upload.wikimedia.org/wikipedia/commons/4/45/Baikal_ice_on_sunset.jpg"
    )
    urllib.request.urlretrieve(big_baikal_url, big_baikal_filename)
    dhash_big_baikal = DHash(big_baikal_filename)
    os.remove(big_baikal_filename)

    small_baikal_filename = os.path.join(this_dir, "baikal_small.jpeg")
    small_baikal_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Baikal_ice_on_sunset.jpg/640px-Baikal_ice_on_sunset.jpg"
    urllib.request.urlretrieve(small_baikal_url, small_baikal_filename)
    dhash_small_baikal = DHash(small_baikal_filename)
    os.remove(small_baikal_filename)

    # Image Attribution: Benh LIEU SONG (Flickr)
    # https://www.flickr.com/photos/blieusong/48128094843/
    yick_cheong_building_filename = os.path.join(this_dir, "yick_cheong_building.jpeg")
    yick_cheong_building__url = "https://upload.wikimedia.org/wikipedia/commons/c/c7/Looking_upward_at_the_Yick_Cheong_Building%2C_13_June_2019.jpg"
    urllib.request.urlretrieve(yick_cheong_building__url, yick_cheong_building_filename)
    dhash_yick_cheong_building = DHash(yick_cheong_building_filename)
    os.remove(yick_cheong_building_filename)

    assert dhash_big_baikal != dhash_yick_cheong_building
    assert dhash_small_baikal == dhash_big_baikal
    assert (dhash_small_baikal - dhash_big_baikal) == 0
    assert (dhash_small_baikal - dhash_yick_cheong_building) > 0
    assert (
        dhash_big_baikal
        - "0b0011111010011110111110100001001111001101010011100000011100101011"
    ) == 0
    assert (dhash_small_baikal - "0x3e9efa13cd4e072b") == 0
    assert (dhash_small_baikal - str(dhash_big_baikal)) == 0
    assert (dhash_small_baikal - dhash_big_baikal.hash) == 0
    assert len(dhash_small_baikal) == 66
    assert "DHash" in repr(dhash_big_baikal)
    assert (dhash_big_baikal - dhash_small_baikal.hash_hex) == 0
    assert dhash_big_baikal.bits_in_hash == 64

    # The value of hash here does not start with 0b or 0x
    with pytest.raises(TypeError):
        assert dhash_big_baikal - "01011010101010101"

    # the length of the binary value is less than the 64 bits, the default
    with pytest.raises(ValueError):
        assert dhash_big_baikal - "0b01011010101010101"

    # Prevent end user from passing None for difference
    with pytest.raises(TypeError):
        assert dhash_big_baikal - None

    # clearly both the Images are same but of different resolution
    with pytest.raises(AssertionError):
        assert dhash_big_baikal != dhash_small_baikal

    # only DHash instance, binary and hex are allowed not integer.
    with pytest.raises(TypeError):
        (dhash_big_baikal - 999999)

    # just a made up name that mostly linke will not exist on this test directory
    with pytest.raises(FileNotFoundError):
        thisfiledoesnotexists = os.path.join(this_dir, "thisfiledoesnotexists.jpg")
        DHash(thisfiledoesnotexists)

    with pytest.raises(ValueError):
        DHash.hex2bin("64", 10)

    with pytest.raises(ValueError):
        DHash.hamming_distance("abcd", "abc")

    with pytest.raises(ValueError):
        DHash.bin2hex("10101")
