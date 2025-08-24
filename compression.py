import heapq
import os

# step 1 create a tree node 
class Node:
    def __init__(self,char,freq):
        self.char=char
        self.freq=freq
        self.left=None
        self.right=None
        
    def __lt__(self,other):
        return self.freq <other.freq

class Huffmancoding:
    def __init__(self,path):
        self.path=path
        self.codes={}
        self.reverse_mapping={}
    # make a frequency map or dictionary    
    def frequency_dict(self,text):
        frequency={}
        for character in text:
            if not character in frequency:
                frequency[character]=0
            frequency[character]+=1
        return frequency
    # make a heap
    def heap(self,frequency):
        heap=[]
        for key,freq in frequency.items():
            heapq.heappush(heap,Node(key,freq))
        return heap
    #merge nodes to form a tree
    def merge(self,heap):
        while len(heap)>1:
            node1=heapq.heappop(heap)
            node2=heapq.heappop(heap)
            merge=Node(None,node1.freq+node2.freq)
            merge.left=node1
            merge.right=node2
            heapq.heappush(heap,merge)
        return heap
    #make a code generator
    def code_helper(self,root,currentcode):
        if root==None:
            return
        if root.char is not None:
            self.codes[root.char]=currentcode
            self.reverse_mapping[currentcode]=root.char
            return
        self.code_helper(root.left,currentcode+"0")
        self.code_helper(root.right,currentcode+"1")
    def make_codes(self,heap):
        root=heapq.heappop(heap)
        self.code_helper(root,"")
    # encode the text
    def get_encode(self,text):
        return "".join(self.codes[ch] for ch in text)
    # add padding to make byte-sized data
    def pad_encode(self,encode):
        extra= 8-len(encode)%8
        for i in range(extra):
            encode+="0"
        pad_info="{0:08b}".format(extra)
        encode=encode+pad_info
        return encode
    # convert into byte array
    def get_bytearray(self,pencode):
        if len(pencode)%8!=0:
            print("Encoded text not padded properly")
            exit(0)
        a=bytearray()
        for i in range(0,len(pencode),8):
            byte=pencode[i:i+8]
            a.append(int(byte,2))
        return a
    def compress(self):
        filename,file_extension=os.path.splitext(self.path)
        output_path=filename+ ".bin"
        with open(self.path,"r") as file:
            text=file.read()
        frequency=self.frequency_dict(text)
        heap=self.heap(frequency)
        heap=self.merge(heap)
        self.make_codes(heap)
        encode=self.get_encode(text)
        pad_encode=self.pad_encode(encode)
        a=self.get_bytearray(pad_encode)
        with open(output_path,"wb") as output:
            output.write(bytes(a))
        print("Compressed file :",output_path)
        return output_path
    def remove(self,pad_encode):
        pad_info=pad_encode[:8]
        extra=int(pad_info,2)
        # removing padding info
        pad_encode=pad_encode[8:]
        encode=pad_encode[:-extra]
        return encode
    def decode(self,encode):
        currentcode=""
        decode=""
        for bit in encode:
            currentcode+=bit
            if currentcode in self.reverse_mapping:
                decode+=self.reverse_mapping[currentcode]
                currentcode=""
        return decode    
    def decompress(self,input_path):
        filename,file_extension=os.path.splitext(self.path)
        output_path=filename + "_decompressed.txt"
        with open(input_path,"rb") as file:
            bit_string=""
            byte=file.read(1)
            while byte:
                byte=ord(byte)
                bits=bin(byte)[2:].rjust(8,"0")
                bit_string+=bits
                byte=file.read(1)
            encode=self.remove(bit_string)
            decompressed=self.decode(encode)
            with open(output_path,"w") as output:
                output.write(decompressed)
            print("decompressed file: ",output_path)
            return output_path
        
        
        
    

if __name__ == "__main__":
    path="temp.py"
    h=Huffmancoding(path)
    compressed_file=h.compress()
    h.decompress(compressed_file)
    
    