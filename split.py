import os
import shutil
import random
from pathlib import Path

def create_train_test_dirs(base_path, classes):
    """
    Membuat struktur direktori train dan test di dalam folder yolo_dataset
    """
    # Membuat direktori yolo_dataset jika belum ada
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    
    # Membuat direktori train dan test
    for split in ['train', 'test']:
        split_path = os.path.join(base_path, split)
        if not os.path.exists(split_path):
            os.makedirs(split_path)
            
        # Membuat subdirektori untuk setiap kelas
        for cls in classes:
            class_path = os.path.join(split_path, cls)
            if not os.path.exists(class_path):
                os.makedirs(class_path)

def split_dataset(dataset_path, train_ratio=0.8, random_seed=42):
    """
    Split dataset menjadi train dan test set dengan mempertahankan struktur folder
    dalam direktori yolo_dataset
    
    Args:
        dataset_path: Path ke direktori dataset
        train_ratio: Rasio data training (default: 0.8)
        random_seed: Random seed untuk reproducibility
    """
    # Set random seed
    random.seed(random_seed)
    
    # Mendapatkan path absolut
    dataset_path = os.path.abspath(dataset_path)
    parent_dir = os.path.dirname(dataset_path)
    
    # Membuat direktori yolo_dataset
    yolo_dataset_path = os.path.join(parent_dir, 'yolo_dataset')
    
    # Mendapatkan nama-nama kelas (folder di dalam dataset)
    classes = [d for d in os.listdir(dataset_path) 
              if os.path.isdir(os.path.join(dataset_path, d))]
    
    print(f"Kelas yang ditemukan: {classes}")
    
    # Membuat direktori train dan test di dalam yolo_dataset
    create_train_test_dirs(yolo_dataset_path, classes)
    
    # Proses setiap kelas
    for cls in classes:
        print(f"\nMemproses kelas: {cls}")
        
        # Path ke direktori kelas
        class_path = os.path.join(dataset_path, cls)
        
        # Mendapatkan semua file dalam kelas
        files = [f for f in os.listdir(class_path) 
                if os.path.isfile(os.path.join(class_path, f))]
        
        # Mengacak urutan file
        random.shuffle(files)
        
        # Menghitung jumlah file untuk training
        n_train = int(len(files) * train_ratio)
        
        # Membagi file menjadi train dan test
        train_files = files[:n_train]
        test_files = files[n_train:]
        
        print(f"Total file: {len(files)}")
        print(f"File training: {len(train_files)}")
        print(f"File testing: {len(test_files)}")
        
        # Memindahkan file ke direktori train dalam yolo_dataset
        for f in train_files:
            src = os.path.join(class_path, f)
            dst = os.path.join(yolo_dataset_path, 'train', cls, f)
            shutil.copy2(src, dst)
            
        # Memindahkan file ke direktori test dalam yolo_dataset
        for f in test_files:
            src = os.path.join(class_path, f)
            dst = os.path.join(yolo_dataset_path, 'test', cls, f)
            shutil.copy2(src, dst)

if __name__ == "__main__":
    # Path ke direktori dataset
    dataset_path = "dataset"
    
    # Melakukan split dataset
    split_dataset(dataset_path)
    
    print("\nPemisahan dataset selesai!")