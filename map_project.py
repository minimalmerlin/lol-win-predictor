import os

def print_tree(startpath):
    ignore_dirs = {'.git', 'node_modules', '.next', '__pycache__', 'venv', 'env', '.DS_Store', 'crawler_state'}
    
    for root, dirs, files in os.walk(startpath):
        # Filter ignoriertes Zeug
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if f.endswith(('.ts', '.tsx', '.py', '.json', '.js')) and f != 'package-lock.json':
                print(f'{subindent}{f}')

if __name__ == "__main__":
    print_tree('.')