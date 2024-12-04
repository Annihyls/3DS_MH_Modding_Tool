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

import os
import zlib
import binascii

from .util import *

ext = {
    # MH4G
    b"97f9db41": ".caff",
    b"982a862b": ".xfs",
    b"6582ee4d": ".xfs",
    b"7784213d": ".xfs",
    b"943b6e23": ".edt",
    b"b916600c": ".htd",
    b"16bf5b52": ".esq",

    # MHX
    b"050d8573": ".arc",
    b"4020c539": ".lcm",
    b"ffe72600": ".ccl",
    b"9f965d53": ".ctc",
    b"9f77fc51": ".sbc",
    b"1774394e": ".ean",
    b"54e85a6d": ".efl",
    b"02baab3a": ".emc",
    b"d4480e0a": ".emd",
    b"acbb8b3d": ".etd",
    b"719a8660": ".evt",
    b"2255c311": ".gr2",
    b"41fb8d62": ".gr2s",
    b"f2bc3704": ".grw",
    b"3f69fd25": ".ipl",
    b"b16a7752": ".ips",
    b"f42e3015": ".lyt",
    b"28008e70": ".lanl",
    b"d2c31635": ".lfd",
    b"01054462": ".lmd",
    b"15ee5637": ".ptex",
    b"25192b68": ".lfx",
    b"e6c8b514": ".sbk",
    b"8630ea7b": ".cfl",
    b"3fde1826": ".srq",
    b"7c674b4a": ".rev_ctr",
    b"2e5a1967": ".mca",
    b"4d5a6a3a": ".stq",
    b"3329cd68": ".ses",
    b"6e1a176e": ".mss",
    b"a8c84927": ".mrl",
    b"896f8b14": ".mef",
    b"5658a158": ".mod",
    b"810d8276": ".lmt",
    b"d693f631": ".moflex",
    b"8ed1bf1b": ".mib",
    b"39b80d4c": ".sdl",
    b"ce7c4307": ".ase",
    b"f47dcd0e": ".scs",
    b"1fe81503": ".sds",
    b"ee00882a": ".sai",
    b"f9a2416b": ".scd",
    b"d5755306": ".sis",
    b"078d2719": ".skst",
    b"5e6dc570": ".skmt",
    b"a9ee592c": ".sksg",
    b"eb5d1f24": ".tex",
    b"59b6365f": ".way",
    b"00b6547b": ".atd",
    b"8e4d2a3e": ".amlt",
    b"f5920600": ".amskl",
    b"013ef321": ".amslt",
    b"b0030279": ".angryprm",
    b"e02e2e7f": ".areaacttbl",
    b"64ede11e": ".areacmnlink",
    b"d092d856": ".areaeatdat",
    b"1282f76f": ".areainfo",
    b"6f4ff84b": ".arealinkdat",
    b"c8f34709": ".areapatrol",
    b"218de915": ".areaseldat",
    b"7e327e32": ".abd",
    b"f5347273": ".acd",
    b"3ce0513c": ".ard",
    b"b2a17c01": ".ased",
    b"0ab69678": ".asd",
    b"2db5c71a": ".bdd",
    b"19958e36": ".bgsd",
    b"7f386a5f": ".cms",
    b"7eb17d0a": ".deco",
    b"ec9a141f": ".mdd",
    b"f892ca32": ".esl",
    b"2c69dc5a": ".emsizetbl",
    b"37eb0018": ".emyure",
    b"dac3d959": ".dtb",
    b"1e29bc1b": ".dtp",
    b"29ace848": ".dtt",
    b"bbd70e63": ".nan",
    b"b0703f58": ".rdb",
    b"42d32b25": ".ebcd",
    b"7c364145": ".pts",
    b"461f9930": ".frl",
    b"3eb94325": ".ses",
    b"43e8eb10": ".mss",
    b"fc020e3e": ".fsh",
    b"228f6f49": ".fup",
    b"7b32c706": ".fmt",
    b"85806a15": ".fmi",
    b"a403c261": ".fms",
    b"94839422": ".gui",
    b"0026462d": ".gfd",
    b"af68f707": ".gii",
    b"9ab22b24": ".gmd",
    b"144ea833": ".hgi",
    b"ba64bb70": ".hde",
    b"08f02e4e": ".hdp",
    b"ee8cb64e": ".hds",
    b"b0c15356": ".hts",
    b"8d5e4a29": ".hta",
    b"3a241c14": ".insectabirity",
    b"814e5338": ".isa",
    b"f69ede11": ".isd",
    b"355e766e": ".insectessenceskill",
    b"3869b148": ".isl",
    b"a2d9a176": ".isp",
    b"a883487c": ".itm",
    b"f36b8e5b": ".itp",
    b"2424f663": ".ipt",
    b"762f976e": ".kad",
    b"7f06dd02": ".kod",
    b"0434e341": ".lan",
    b"7a4d7e19": ".maptime",
    b"7ee7d07c": ".mpm",
    b"ddcf816d": ".oar",
    b"36e8514b": ".olvl",
    b"06ab0f0c": ".otml",
    b"68aaa65e": ".oxpb",
    b"6ff73970": ".oxpv",
    b"52c0860f": ".oskl",
    b"60605e7c": ".osa",
    b"b75c397a": ".sab",
    b"67671c2f": ".saou",
    b"c65c283c": ".otd",
    b"8ad70d5b": ".otp",
    b"74a71f68": ".owp",
    b"1d903951": ".plbasecmd",
    b"d32b4c4b": ".plcmdtbllist",
    b"4d2c3a23": ".plgmktype",
    b"5c22a918": ".pma",
    b"d29ec866": ".plpartsdisp",
    b"c1490d54": ".plweplist",
    b"e3160a45": ".pntpos",
    b"d47acc6f": ".pec",
    b"165c525a": ".pel",
    b"c9094325": ".psl",
    b"5097ed20": ".pep",
    b"af79cf61": ".qsg",
    b"5c12c86e": ".raps",
    b"fc9e321e": ".rlt",
    b"2d303c5b": ".rem",
    b"36210758": ".sfsa",
    b"1d705325": ".sem",
    b"99436d0c": ".sid",
    b"7298a64a": ".shell",
    b"382cb11e": ".sep",
    b"68dcc839": ".skd",
    b"e342394c": ".skt",
    b"fb82d715": ".sbkr",
    b"8fae402b": ".equr",
    b"6649cc1b": ".srqr",
    b"8c222e23": ".revr_ctr",
    b"597bc479": ".mca",
    b"ffbb7d16": ".stqr",
    b"e2880671": ".squs",
    b"ee9a5354": ".sup",
    b"8624a274": ".spval",
    b"22ff1a75": ".tams",
    b"2b039941": ".w00d",
    b"04777d43": ".w00d",
    b"cb2c4829": ".w00m",
    b"6817e256": ".w01d",
    b"3a1cbf2c": ".w01d",
    b"552ce265": ".w01m",
    b"ad2b6f6f": ".w02d",
    b"39a78847": ".w02d",
    b"b62b6d6b": ".w02m",
    b"ee3f1478": ".w03d",
    b"07cc4a28": ".w03d",
    b"282bc727": ".w03m",
    b"2752751c": ".w04d",
    b"7ed7964a": ".w04d",
    b"3122022d": ".w04m",
    b"a17a8332": ".w06d",
    b"4307634e": ".w06d",
    b"4c25276f": ".w06m",
    b"e26ef825": ".w07d",
    b"7d6ca121": ".w07d",
    b"d2258d23": ".w07m",
    b"33a1417a": ".w08d",
    b"f037aa50": ".w08d",
    b"7e37ad7a": ".w08m",
    b"70b53a6d": ".w09d",
    b"ce5c683f": ".w09d",
    b"e0370736": ".w09m",
    b"15685b2e": ".w10d",
    b"c4a8f302": ".w10d",
    b"8838333e": ".w10m",
    b"567c2039": ".w11d",
    b"fac3316d": ".w11d",
    b"16389972": ".w11m",
    b"9340ad00": ".w12d",
    b"f9780606": ".w12d",
    b"f53f167c": ".w12m",
    b"d054d617": ".w13d",
    b"c713c469": ".w13d",
    b"6b3fbc30": ".w13m",
    b"1939b773": ".w14d",
    b"be08180b": ".w14d",
    b"7236793a": ".w14m",
    b"99412e5d": ".ane",
    b"a1f5043b": ".ape",
    b"42ce8a05": ".acn",
    b"13dd2275": ".arcd",
    b"0dd7f263": ".apd",
    b"1545b50a": ".bui",
    b"ec672754": ".cskd",
    b"6b19a101": ".doi",
    b"51d02922": ".dcd",
    b"93dba65c": ".sla00",
    b"51040d44": ".slw00",
    b"c7340a33": ".slw01",
    b"7d65032a": ".slw02",
    b"eb55045d": ".slw03",
    b"48c06043": ".slw04",
    b"64a16e2d": ".slw06",
    b"f291695a": ".slw07",
    b"638cd64a": ".slw08",
    b"f5bcd13d": ".slw09",
    b"1035165d": ".slw10",
    b"8605112a": ".slw11",
    b"3c541833": ".slw12",
    b"aa641f44": ".slw13",
    b"09f17b5a": ".slw14",
    b"f070166a": ".fld",
    b"ff0f0824": ".fht",
    b"77ac1258": ".gpd",
    b"4303d777": ".atr",
    b"291cbc58": ".ext",
    b"f8290316": ".rem",
    b"14f34334": ".iaf",
    b"81b20d30": ".igf",
    b"6aada53f": ".ict",
    b"139f3a23": ".kcg",
    b"ea68740c": ".kcm",
    b"194d966d": ".kca",
    b"bf4d6c0c": ".kcr",
    b"87a4f024": ".kcs",
    b"20617e23": ".kc1",
    b"9a30773a": ".kc2",
    b"0c00704d": ".kc3",
    b"8acdd766": ".mai",
    b"e56c417f": ".mcn",
    b"d07c7d11": ".mcm",
    b"c494c919": ".mex",
    b"3858027d": ".mla",
    b"3f81682a": ".mlc",
    b"b9dd914a": ".mle",
    b"844d8464": ".mri",
    b"fd09c936": ".mre",
    b"d6c46b62": ".mrs",
    b"d7251904": ".mvp",
    b"39aa5a6d": ".npcBd",
    b"332a0643": ".npcId",
    b"31c69a69": ".npcMdl",
    b"5d073004": ".nis",
    b"ff604f16": ".nld",
    b"7b528834": ".npcMd",
    b"8b3e271a": ".npcSd",
    b"ba9c3e1a": ".ntd",
    b"81fd2006": ".oec",
    b"93b8cf2b": ".otil",
    b"6925577b": ".olsk",
    b"c911ff79": ".olos",
    b"42b4566f": ".opl",
    b"df25b569": ".otpt",
    b"eadace10": ".pcl",
    b"c40ba625": ".ssjje",
    b"71f32c33": ".ssjjp",
    b"df239d61": ".slt",
    b"c8445b5e": ".sls",
    b"78e88d45": ".sad",
    b"de4d3325": ".trdl",
    b"94127529": ".tril",
    b"f5a0fc55": ".tlil",
    b"7d875427": ".trll",
    b"31abf219": ".tpil",
    b"bccd6c05": ".tucyl",
    b"c5c6c02f": ".tuto",
    b"53082262": ".vfp",
    b"c64d3542": ".wcd",
    b"c6e6fc15": ".wpd",
}

rev_ext = dict(list(zip([ex for bin, ex in list(ext.items())], [bin for bin, ex in list(ext.items())])))


class ARC:
    magic = [b'ARC\x00']
    supported_versions = [7, 16, 17, 19]

    def __init__(self, arc=None):
        if arc:
            self.import_arc(arc)
        else:
            self.default_meta()

    def default_meta(self):
        self.magic = ARC.magic[0]
        self.version = 19
        self.file_list = []
        self.file_count = 0

    def import_arc(self, arc):
        self.parse_header(arc)
        self.parse_file_list(arc)
        self.parse_files(arc)

    def parse_header(self, arc):
        self.magic = read_block(arc, 0x00, 0x4)
        if self.magic not in ARC.magic:
            print(ARC.magic)
            print(self.magic)
            error("Invalid Magic Identifier")

        self.version = read_word(arc, 0x04)

        if self.version not in ARC.supported_versions:
            error('Unsupported Version: {}'.format(self.version))

        self.file_count = read_word(arc, 0x06)
        # self.null_bytes = read_dword(arc, 0x08)

    def parse_file_list(self, arc):
        if self.version == 19 or self.version == 17:
            file_table_offset = 0x0C
            file_table_length = 0x50
        elif self.version == 16:
            file_table_offset = 0x0C
            file_table_length = 0x50
        elif self.version == 7:
            file_table_offset = 0x08
            file_table_length = 0x50

        file_list = []

        for idx in range(self.file_count):
            offset = file_table_offset + (idx * file_table_length)
            f = {}
    
            # Lire les blocs en tant que bytes
            f['file'] = read_block(arc, offset + 0, 64)
            f['extension'] = read_block(arc, offset + 64, 4)
            f['size'] = read_dword(arc, offset + 68)
            f['unc_size'] = read_dword(arc, offset + 72)
            f['offset'] = read_dword(arc, offset + 76)

            # Conversion de l'extension en hex (en bytes)
            f['raw_ext'] = binascii.hexlify(f['extension'])

            # Conversion de l'extension en hex, mais avec un format approprié
            f['extension'] = binascii.hexlify(f['extension'])

            # Vérification de l'extension et attribution de l'extension correspondante
            if f['extension'] in ext:
                extension = ext[f['extension']]
            else:
                log_info('Unknown File Signature: {}'.format(f['extension']))
                extension = '.' + f['extension'].decode('utf-8')
            
            print(extension)
            # Remplacement des caractères et ajout de l'extension (f['file'] doit aussi être en bytes)
            f['file'] = f['file'].replace(b"\\", b'/').rstrip(b'\x00') + extension.encode('utf-8')

            # Extraire le nom du fichier et path (si nécessaire)
            # f['path'], f['name'] = os.path.split(f['file'].decode('utf-8'))

            # Calcul de certaines valeurs (sans changement, car elles sont déjà en int)
            f['unk0'] = (f['unc_size'] & 0xFF000000) >> (8 * 3)
            f['unc_size'] = f['unc_size'] & 0xFFFFFF

            # Ajouter le fichier à la liste
            file_list.append(f)

        self.file_list = file_list

    def parse_files(self, arc):
        for f in self.file_list:
            f['data'] = read_block(arc, f['offset'], f['size'])
            try:
                f['data'] = zlib.decompress(memoryview(f['data']))
            except zlib.error as e:
              print("Error decompressing file:", f['file'], "at offset", f['offset'])
              print("Compressed Size:", f['size'], "Uncompressed Size:", f['unc_size'])
              raise

    def export_arc(self):
        arc = bytearray()
        self.write_header(arc)
        self.write_file_list(arc)
        return arc

    def write_header(self, arc):
        alloc_block(arc, 0x1C)
        write_block(arc, 0x0, self.magic)
        write_word(arc, 0x04, self.version)
        write_word(arc, 0x06, len(self.file_list))
        write_dword(arc, 0x08, 0)
        return arc

    def write_file_list(self, arc):
        if self.version == 19 or self.version == 17:
            file_table_offset = 0x0C
            file_table_length = 0x50
        elif self.version == 16:
            file_table_offset = 0x0C
            file_table_length = 0x50
        elif self.version == 7:
            file_table_offset = 0x08
            file_table_length = 0x50

        addr = alloc_block(arc, file_table_length * len(self.file_list) + 4)

        for idx in range(len(self.file_list)):
            offset = file_table_offset + (idx * file_table_length)
            f = self.file_list[idx]

            # compress data
            cdata = zlib.compress(memoryview(f['data']))
            addr = alloc_block(arc, len(cdata))

            filename, extension = os.path.splitext(f['file'])

            if extension == '.mod':
                unc_size = (0xA0 << (8 * 3)) + len(f['data'])
            else:
                unc_size = (0x20 << (8 * 3)) + len(f['data'])

            extension = binascii.unhexlify(f['raw_ext'])

            write_block(arc, addr, cdata)
            write_block(arc, offset + 0, filename.replace('/', '\\').encode('utf-8'))
            write_block(arc, offset + 64, extension)
            write_dword(arc, offset + 68, len(cdata))
            write_dword(arc, offset + 72, unc_size)
            write_dword(arc, offset + 76, addr)

        return arc

    def add_file(self, filename, data, ext):
        f = {}
        f['file'] = filename
        f['raw_ext'] = ext
        f['data'] = data

        self.file_list.append(f)

    def __str__(self):
        info = """ARC
		Version : {version}
		files   : {file_count}""".format(**self.__dict__)
        return info
