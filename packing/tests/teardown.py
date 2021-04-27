import os

def main():
    dest_path = 'packing_lists'
    
    for filename in os.listdir(dest_path):
        path = os.path.join(dest_path, filename)
        os.remove(path)

if __name__ == '__main__':
    main()
