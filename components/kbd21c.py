# (c) OctopusLAB 2020-23
# kbd21c - addr + data / 8 segment display TM1638 + kbd 3x7 


BTN_TAB = {
(4,4,0,0,0): "0",
(2,2,0,0,0): "1",
(1,1,0,0,0): "2",
(64,64,0,0,0):"3",
(32,32,0,0,0):"4",
(16,16,0,0,0):"5",
(2048,0,8,0,0):"6",
(1024,0,4,0,0):"7",
(512,0,2,0,0): "8",
(32768,0,128,0,0):"9",
(16384,0,64,0,0):"A",
(8192,0,32,0,0):"B",
(16,0,0,16, 0):"C",
(8,0,0,8,0): "D",
(4,0,0,4,0): "E",
(256,0,0,256, 0):"F",

(128, 0, 0, 128, 0):"S",
(64, 0, 0, 64, 0):"P",
(16384, 0, 0, 0, 32):"-",
(8192, 0, 0, 0, 16):"R"
}



class Hex2:
    def __init__(self):
        self.characters = ['-', '-']
        self.saved_arr = []
        self.saved_hex2_index = 0


    def add(self, char):
            
        if char == 'S':
            print("DEBUG class:",len(self.saved_arr),self.saved_hex2_index)
            if len(self.saved_arr) < self.saved_hex2_index+1:
                self.saved_arr.append(''.join(self.characters))
                self.saved_hex2_index += 1
            else:
                self.saved_arr[self.saved_hex2_index] = ''.join(self.characters)
        else:
            if len(self.characters) == 2:
                self.characters[0] = self.characters[1]
                self.characters[1] = char
            else:
                self.characters.append(char)


    def dec(self): # decrement index
        self.saved_hex2_index -= 1
        if self.saved_hex2_index < 0:
            self.saved_hex2_index = 0


    def inc(self): # decrement index
        self.saved_hex2_index += 1
        if self.saved_hex2_index > len(self.saved_arr)-1:
            self.saved_hex2_index = len(self.saved_arr)-1
    
    
    def show(self):
        return ''.join(self.characters)
        #  self.saved_hex2[self.cnt-1]  // index-1 (0,1,2...)


    def get_saved_arr(self):
        return self.saved_arr


    def get_saved_hex2(self, index):
        return self.saved_arr[index]
 
 
    def get_saved_program(self):
        ret = ' '.join(self.saved_arr)
        return ret
    
    
    def get_program_num(self):
        program_num = []
        for hex_i in self.saved_arr:
            program_num.append(int("0x"+hex_i))      # int
        return program_num
