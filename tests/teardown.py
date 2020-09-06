import os

dest_path = 'packing_lists'
templates_path = os.path.join('tests', 'templates')

for filename in os.listdir(dest_path):
    path = os.path.join(dest_path, filename)
    os.remove(path)
