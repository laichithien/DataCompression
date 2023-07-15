from Huffman import Huffman
from LZ77 import LZ77
from LZ78 import LZ78
from shannon_fano.shannon_fano import ShannonFano
from LZW import LZW
from huffman_fgk.fgk import FGK
from rle import RLE

test_file_path = 'demo.txt'

LZ77().Metric(test_file_path)
LZ78().Metric(test_file_path)
LZW().Metric(test_file_path)
ShannonFano().Metric(test_file_path)
FGK().Metric(test_file_path)
RLE().Metric(test_file_path)

