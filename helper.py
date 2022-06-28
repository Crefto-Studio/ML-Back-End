def remove_token(token):
    # list to store file lines
    lines = []
    # read file
    try:
        with open("file.txt", 'r') as fp:
            # read an store all lines into list
            lines = fp.readlines()
    except FileNotFoundError:
        with open("file.txt", 'w') as fp:
            pass
    # Write file
    with open("file.txt", 'w') as fp:
        # iterate each line
        deleted_token=-1
        for number, line in enumerate(lines):
            # delete line 5 and 8. or pass any Nth line you want to remove
            # note list index starts from 0
            if line == token+"\n":
                deleted_token =number

            if number != deleted_token:
                fp.write(line)

def add_token(token):
    f=open("file.txt", "a+")
    f.write("%s\n" %(token))
    f.close()

def is_token_found(token):
    token = token + "\n"
    lines = []
    try:
        with open("file.txt", 'r') as fp:
        # read an store all lines into list
            lines = fp.readlines()
            fp.close()  
            if token in lines:
                return True
            else:
                return False     
    except FileNotFoundError:
        return False                         

def resizing_vector(data):

    data = list(data.values()) # to store values only of the input json string
    data_inverse = [255 - x for x in data] # inverse 0 --> 1
    size= int(math.sqrt(len(data_inverse)))
    data_inverse =data_inverse[:size*size]
    data_inverse = np.array(data_inverse)  
    data = np.reshape(data_inverse,(size, size))  
    
    return data
