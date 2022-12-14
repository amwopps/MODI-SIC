import pandas as pd
from instructions import instructions, directives
from utils import open_file, return_df, return_intermediate, return_symbol_table, out_pass1

# Adds Location Counter to the dataframe
def location_counter(df):
    start_index = df.Value[0]
    list_counter = [' ', start_index]
    counter = start_index

    for i in range(1, df.index.stop):

        if df.Mnemonic[i] not in instructions and df.Mnemonic[i] not in directives:
            print('NO INSTRUCTION/DIRECTIVE NAMED {0}'.format(df.Mnemonic[i]))
            quit()
        
        elif df.Mnemonic[i] in instructions:
            # Format 1 instruction
            if type(instructions[df.Mnemonic[i]]) == list:
                temp = hex(int(counter, 16) + 1)

            # Format 3 instruction
            else:
                temp = hex(int(counter, 16) + 3)
        
        if df.Mnemonic[i] == 'WORD':
            temp = hex(int(counter, 16) + 3)

        if df.Mnemonic[i] == 'BYTE':
            value = df.Value[i].split('\'')
            length = len(value[1])
            if value[0] == 'C':
                temp = hex(int(counter, 16) + int(length))
            elif value[0] == 'X':
                temp = hex(int(counter, 16) + int(int(length)/2))
            else:
                print('INVALID VALUE FOR BYTE')
                quit()

        # hex functions deals with integers ONLY
        # Counter is saved as a string hex value
        # int(counter, 16) transforms is to the integer value of the hex value
                
        # df.Value[i] is saved as a string decimal value
        # First, we transform it to integer using int(), then we add it in hex()
                
        if df.Mnemonic[i] == 'RESW':
            temp = hex(int(counter, 16) + int(df.Value[i]) *3)
            
        if df.Mnemonic[i] == 'RESB':
            temp = hex(int(counter, 16) + int(df.Value[i]))
            
            
        # Saving the new counter, and truncating the 0x at the beginning of the hex number
        counter = temp.split('x')[1].rjust(4, '0').upper()
        list_counter.append(counter)
    # Adding the location counter to the dataframe
    df.insert(0, 'Location_Counter', list_counter[:-1])
    return df

# Returns list with symbol table inside of it
def symbol_table(df):
    list = {}
    # Ignoring the first row 
    for i in range(1, df.index.stop):
        if df.Label[i] != ' ':
            if df.Label[i] in list:
                print('LABEL {0} ALREADY EXISTS'.format(df.Label[i]))
                quit()
            list[df.Label[i]] = df.Location_Counter[i]
    return list


def pass_one(path):
    print('-' * 30)
    print('*' *5 + ' PARSING STARTED ' + '*' *5)
    program = open_file(path+ '.txt')
    df = return_df(program)
    return_intermediate(df)
    print('*' *5 + ' PARSING ENDED ' + '*' *5)
    print('-' * 30)
    print("\n")

    print('-' * 30)
    print('*' *5 + ' PASS ONE STARTED '+ '*' *5)
    df = location_counter(df)
    sym_table = symbol_table(df)
    return_symbol_table(sym_table)
    out_pass1(df)
    print('*' *5 + ' PASS ONE ENDED ' + '*' *5)
    print('-' * 30)
    print("\n")
    return df, sym_table
