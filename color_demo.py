# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
from adafruit_funhouse import FunHouse
from colors import rotate


funhouse = FunHouse(
    default_bg=0x282c34,
    scale=4,
)

colors = [0, 1, 2, 3, 4]
palette = [0x800000, 0x808000, 0x008000, 0x000080, 0x800080]
calculated_colors = [palette[color_index] for color_index in colors]
funhouse.peripherals.set_dotstars(*calculated_colors)

# Create the labels
funhouse.display.show(None)

temp_label = funhouse.add_text(
    text="Temp:", text_position=(0, 5), text_color=0x00FF00
)
funhouse.display.show(funhouse.splash)

while True:
    cel_temp = funhouse.peripherals.temperature
    fahr_temp = ((cel_temp * 9) / 5) + 32
    funhouse.set_text("Temp %0.1F C" %
                      cel_temp, temp_label)

    calculated_colors = []
    for i in range(5):
        color_index = colors[i]
        color = palette[color_index]
        colors[i] += 1
        colors[i] %= 5

        calculated_colors.append(color)

    funhouse.peripherals.set_dotstars(*calculated_colors)
