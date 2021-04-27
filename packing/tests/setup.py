import os
import shutil

def main():
    dest_path = 'packing_lists'
    templates_path = os.path.join('packing', 'tests', 'templates')
    
    for filename in os.listdir(templates_path):
        src = os.path.join(templates_path, filename)
        dest = os.path.join(dest_path, filename)
        shutil.copy(src, dest)

if __name__ == '__main__':
    main()