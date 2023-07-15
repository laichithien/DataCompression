import streamlit as st
# import re
# import sys
from math import log10
# from symspellpy import SymSpell,  Verbosity
from collections import Counter
import numpy as np
# import streamlit_scrollable_textbox as stx
from shannon_fano.shannon_fano import ShannonFano
from range_coding.range_coding import RangeCoding
from LZ78 import LZ78
from LZ77 import LZ77
from LZW import LZW
from rle import RLE
from huffman_fgk.fgk import FGK



def load_file(filename):
    with open(filename, encoding="utf8") as f:
        lines = f.readlines()
    #print("No of sentences in Corpus: "+str(len(lines)))
    f.close()
    return lines

st.title('Nén dữ liệu')
col1, col2 = st.columns(2)
option,algothirm,uploaded_files,text = 0,0,0,0
with col1:
    algothirm = st.selectbox(
    'Select algothirm:',
    ('RLE', 'Huffman_fgk', 'Shannon Fano','Range Coding','LZ77','LZ78','LZW'))

with col2:
    option= st.radio(
        "Select input source:",
        options=["Input text"],
    )

if option == "File":
    uploaded_files = st.file_uploader("Please select input file.")
else:
    text = st.text_input('Input text', '')

if st.button('Encode'):
    if option == "Input text":
        if algothirm == 'RLE':
            output = 'Result: ' + RLE().encode(text)
            st.write(output)
        if algothirm == 'LZ78':
            alg = LZ78()
            output = 'Result: ' + alg.encode(text)
            st.write(output)
        if algothirm == 'LZ77':
            output = 'Result: ' + LZ77().encode(text)
            st.write(output)
        if algothirm == 'LZW':
            output = 'Result: ' + LZW().encode(text)
            st.write(output)
        if algothirm == 'Shannon Fano':
            encoded_shano, table_shano = ShannonFano().encode(text)
            output = 'Result: ' + encoded_shano
            st.write(output)
            st.write("Table:")
            st.write(table_shano)
        if algothirm == 'Range Coding':
            encoded_raco, table_raco, length_raco = RangeCoding().encode(text)
            output = 'Result: ' + str(encoded_raco)
            st.write(output)
            st.write("Table:")
            st.write(table_raco)
            st.write("Length:")
            st.write(table_raco)
        if algothirm == 'Huffman_fgk':
            encoded_fgk = FGK().encode(text)
            output = 'Result: ' + encoded_fgk 
            st.write(output)
            #decoded_fgk = FGK().decode(encoded_fgk)
            #decoded_raco = RangeCoding().decode(encoded_raco, table_raco, length_raco)

if algothirm == 'RLE' or algothirm == 'LZW' or algothirm == 'LZ77' or algothirm == 'LZ78':
    if st.button('Decode'): 
        if option == "Input text":
            if algothirm == 'RLE':
                output = 'Result: ' + RLE().decode(text)
                st.write(output)
            if algothirm == 'LZ78':
                output = 'Result: ' + LZ78().decode(text)
                st.write(output)
            if algothirm == 'LZ77':
                output = 'Result: ' + LZ77().decode(text)
                st.write(output)
            if algothirm == 'LZW':
                output = 'Result: ' + LZW().decode(text)
                st.write(output)
if False:
    if st.button('Correct'):
        if option == "Input text":
            if algothirm == "Bi-gram":
                output = 'Result: '+demo.Correct_sentence(text,alpha=3)
                st.write(output)
            else:
                output = 'Result: '+symspell.Correct_Sentence(text)
                st.write(output)
        else:
            st.write('Result: ')
            results = 0
            if algothirm == "Bi-gram":
                demo.Spelling_Corrector(file_in= uploaded_files.name , file_out = "output.txt", alpha = 3)
                results = load_file("output.txt")
                stx.scrollableTextbox(results,height = 300)
            else:
                symspell.Spelling_Correct(uploaded_files.name , "output.txt")
                results = load_file("output.txt")
                stx.scrollableTextbox(results,height = 300)
        
