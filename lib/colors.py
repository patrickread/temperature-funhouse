def to_base(n):
    return "{:06x}".format(n)


def get_rgbs(hex: int):
    hex_string = to_base(hex)
    r = int(hex_string[0:2], 16)
    g = int(hex_string[2:4], 16)
    b = int(hex_string[4:6], 16)

    return [r, g, b]

def rotate(hex: int):
    red, green, blue = get_rgbs(hex)
    if red > 0:
        red += 15
        if red > 255:
            red = 0
            green = 15

    if green > 0:
        green += 15
        if green > 255:
            green = 0
            blue = 15

    if blue > 0:
        blue += 15
        if blue > 255:
            blue = 0
            red = 15

    return int("0x{red:02x}{green:02x}{blue:02x}".format(red=red, green=green, blue=blue), 16)
