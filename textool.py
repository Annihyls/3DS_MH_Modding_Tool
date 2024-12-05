#!/usr/bin/python
# Copyright 2016 dasding
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PIL import Image, ImageDraw
import argparse
import os

from lib.util import *
from lib.texutil import *
from lib.tex import TEX


def extract(filename, mipmaps, debug):
    tex = TEX(readFile(filename))
    log_info(tex)

    if mipmaps:
        for idx, mipmap in enumerate(tex.mipmaps):
            fn = "{}_{}.png".format(filename, idx)
            writeImage(fn, mipmap)
    else:
        if tex.alpha:
            fn = "{}.alpha.png".format(filename)
            writeImage(fn, tex.alpha_mipmap)
            fn = "{}.png".format(filename)
            writeImage(fn, tex.noalpha_mipmap)
        else:
            fn = "{}.png".format(filename)
            writeImage(fn, tex.mipmaps[0])

    writeFile(filename + '.meta', tex.export_meta())

def create(filename, mipmaps, texformat=None):
    filename = filename.replace(".png", "")
    tex = TEX()
    tex.import_meta(readFile(filename + '.meta'))

    if texformat:
        tex.format = texformat

    log_info(tex)

    if mipmaps:
        for idx in range(tex.mipmap_count):
            fn = '{}_{}.png'.format(filename, idx)
            image = readImage(fn)
            tex.add_mipmap(image)
    else:
        fn = '{}.png'.format(filename)
        image = readImage(fn)

        if tex.alpha:
            fn = "{}.alpha.png".format(filename)
            alpha = readImage(fn)

            image = mux_alpha(image, alpha)
        tex.add_mipmap(image)

        for mipmap_level in range(1, tex.mipmap_count):
            width = image.width // (2**mipmap_level)
            height = image.height // (2**mipmap_level)
            mipmap = image.resize((width, height), resample=Image.Resampling.LANCZOS)
            tex.add_mipmap(mipmap)

    writeFile(filename, tex.export_tex())


def display(filename):
    tex = TEX()
    f = readFile(filename)
    tex.parse_meta(f)

    print(tex)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract and create MT Mobile Framework .tex files")
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-x", "--extract", action="store_true", help="extract a texture")
    group.add_argument("-c", "--create", action="store_true", help="create a texture")

    formatgroup = parser.add_mutually_exclusive_group()
    formatgroup.add_argument("-r", "--rgb", action="store_true", help="export texture in rgb format")
    formatgroup.add_argument("-ra", "--rgba", action="store_true", help="export texture in rgba format")
    formatgroup.add_argument("-ra4", "--rgba4", action="store_true", help="export texture in rgba4 format")
    formatgroup.add_argument("-ea", "--etc1a", action="store_true", help="export texture in etc1a format")

    parser.add_argument("-m", "--mipmaps", action="store_true", help="generate mipmaps")
    parser.add_argument("-d", "--debug", action="store_true", help="overlay debug markers")
    parser.add_argument("-v", "--verbose", action="count", help="increase output verbosity")
    parser.add_argument("input", nargs="+", help="input/output handle")

    args = parser.parse_args()

    enable_log(args.verbose)

    texformat = None
    if args.rgba:
        texformat = 3
    elif args.rgba4:
        texformat = 1
    elif args.rgb:
        texformat = 17
    elif args.etc1a:
        texformat = 12

    for filename in args.input:
        if args.create:
            create(filename, args.mipmaps, texformat)
        elif args.extract:
            extract(filename, args.mipmaps, args.debug)
        else:
            display(filename)
