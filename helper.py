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

  