"""
====[ l-n-s-y's iNES ROM file mapper ]====

started: 05/06/2024


iNES file format spec found @ https://www.nesdev.org/wiki/INES



==[ TODO ]==
    - Add NES 2.0 support

"""


import sys,os

from chr_parser import chr_parser


# iNES section sizes
HEADER_SIZE = 16
SIXTEEN_KB = 16384
EIGHT_KB = 8192



class rom_mapper:
    def __init__(self):
        self.header_mapped = False
        self.prg_mapped = False
        self.chr_mapped = False
        self.read_offset = 0

    def load_rom(self,data):
        self.rom_data = data

    def signature_is_valid(self,sig:bytes) -> bool:
        return sig == b"\x4E\x45\x53\x1A" # "NES\x1a"

    def map_header(self) -> bool: #,section:bytes) -> bool:
        section = self.rom_data[:HEADER_SIZE]
        signature = section[:4]
        if not self.signature_is_valid(signature):
            print("ERROR: Invalid Signature")
            return False
        print(f"\tROM Signature: {signature}")

        self.prg_rom_size = section[4]
        print(f"\tPRG_ROM SIZE: {self.prg_rom_size*SIXTEEN_KB}")
        self.chr_rom_size = section[5]
        self.uses_chr_ram = self.chr_rom_size == 0

        #self.chr_rom_size == b"0":
        if self.uses_chr_ram:
            print("\tBoard uses CHR RAM")
        else:
            print(f"\tCHR_ROM SIZE: {self.chr_rom_size*EIGHT_KB}")

        flags_6 = section[6]
        self.map_flags6(flags_6)
        flags_7 = section[7]
        self.map_flags7(flags_7)

        if self.using_nes2:
            # TODO: NES2.0 support
            # if using nes2: bytes 8-15 are in nes2 format

            # Should mask off higher 4 bits of mapper number
            # and maybe refuse to load ROM
            pass

        flags_8 = section[8]
        self.map_flags8(flags_8)
        flags_9 = section[9]
        self.map_flags9(flags_9)
        flags_10 = section[10]
        self.map_flags10(flags_10)

        self.unused_padding = section[11:15]
        if sum([b for b in self.unused_padding]) != 0: 
            print(f"\tFound unexpected data in 11-15: {self.unused_padding}")

        self.header_mapped = True
        self.read_offset = HEADER_SIZE

    def map_flags6(self,f):
        print("\tMapping FLAGS6 section: ")
        # Arrangement: True -> Vertically Mirrored ; False -> Horizontally Mirrored
        self.nametable_arrangement = "vertical" if (f&0b1) == 1 else "horizontal"
        print(f"\t\tNametable Arr: {self.nametable_arrangement}")

        self.has_battery_RAM = (f&0b10) == 1
        print(f"\t\tHas Battery RAM: {self.has_battery_RAM}")

        self.has_trainer = (f&0b100) == 1
        print(f"\t\tHas Trainer: {self.has_trainer}")

        self.alt_nametable_layout = (f&0b1000) == 1
        print(f"\t\tAlt Nametable Layout: {self.alt_nametable_layout}")

        self.mapper_num_lo = (f&0b11110000)
        print(f"\t\tMapper number lowbyte: {self.mapper_num_lo}")



    def map_flags7(self,f):
        print("\tMapping FLAGS7 section: ")
        self.vs_unisystem = (f&0b1) == 1
        print(f"\t\tVS Unisystem: {self.vs_unisystem}")
        
        self.playchoice10 = (f&0b10) == 1
        print(f"\t\tPlaychoice10: {self.playchoice10}")

        self.using_nes2 = (f&0b1100) == 2
        print(f"\t\tUsing NES 2.0 format: {self.using_nes2}")

        self.mapper_num_hi = (f&0b11110000)
        print(f"\t\tMapper number highbyte: {self.mapper_num_hi}")



    def map_flags8(self,f):
        print("\tMapping FLAGS8 section: ")
        self.prg_ram_compat = f == 0
        if self.prg_ram_compat:
            # Uses 8kb of PRG RAM for compatability
            print(f"\t\tPRG RAM COMPATABILITY")
        self.prg_ram_size = f
        print(f"\t\tPRG RAM Size: {self.prg_ram_size}")


    def map_flags9(self,f):
        print("\tMapping FLAGS9 section: ")

        # Very few emulators honor this bit:
        self.tv_system = "pal" if (f&0b1) == 1 else "ntsc"
        print(f"\t\tTV System: {self.tv_system}")

        reserved = f&0b11111110



    def map_flags10(self,f):
        if 1==1: return # Currently disabled

        tv_sys = (f&0b11)
        if tv_sys == 0:
            self.tv_system = "ntsc"
        elif tv_sys == 2:
            self.tv_system = "pal"
        elif tv_sys == 1 or tv_sys == 3:
            self.tv_system = "dual"




    def map_trainer(self):
        self.trainer = self.rom_data[self.read_offset:self.read_offset+512]
        self.read_offset += 512


    def map_prg_rom(self):
        index_offset = (self.prg_rom_size*SIXTEEN_KB)
        self.prg_rom = self.rom_data[self.read_offset:self.read_offset+index_offset]

        self.read_offset += index_offset

        self.prg_mapped = True


    def map_chr_rom(self):
        index_offset = (self.chr_rom_size*EIGHT_KB)
        self.chr_rom = self.rom_data[self.read_offset:self.read_offset+index_offset]

        self.read_offset += index_offset

        self.chr_mapped = True


    def map_prg_ram(self):
        # RAM Size: self.prg_ram_size * EIGHT_KB
        pass


def main(rom_file):
    with open(rom_file,"rb") as f:
        rom_data = f.read()

    print(f"Parsing ROM: {rom_file}")
    new_rom = rom_mapper()
    new_rom.load_rom(rom_data)
    #new_rom.map_header(rom_data[:HEADER_SIZE])
    new_rom.map_header()


    if new_rom.has_trainer:
        new_rom.map_trainer()

    new_rom.map_prg_rom()

    if not new_rom.uses_chr_ram:
       new_rom.map_chr_rom()
    else:
        print("ROM uses CHR RAM. (not currently supported)")
        exit()

    chr_prsr = chr_parser()
    chr_prsr.parse_tiles(new_rom.chr_rom)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} [nes_rom]")
        exit()

    if not os.path.exists(sys.argv[1]):
        print(f"Error: rom file doesn't exist")
        exit()

    rom_file = sys.argv[1]

    main(rom_file)
