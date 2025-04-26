

def xor(data, key) -> str: 
  
    # calculate length of data string 
    length = len(data)
  
    # perform XOR operation of key 
    # with every character in string 
    for i in range(length):
        data = (data[:i] + 
             chr(ord(data[i]) ^ ord(key)) +
                     data[i + 1:])
      
    return data