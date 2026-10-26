from pathlib import Path
import shutil
import os
import hashlib
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool

images = []
docs = []
video = []
audio = []
others = []
dublicats = []
all_hashe = []

def mainn():
    main_path = input("Enter Main Folder Path: ")
    global current_folder, target_image, target_doc, target_vedio, target_audio, target_other
    current_folder = Path(main_path)
    # Target paths defined here after getting current_folder
    target_image = current_folder/"Image"
    target_doc = current_folder/"Documents"
    target_vedio = current_folder/"Vedio"
    target_audio = current_folder/"Audio"
    target_other = current_folder/"Other"

    for file in current_folder.iterdir():
        if file.is_dir():
            continue
        file_name = file.name  #with extension
        file_size = file.stat().st_size
        file_ext = file.suffix.lower()

        x = hashlib.sha256()
        with open(str(file),"rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                x.update(chunk)
        file_hash = x.hexdigest()

        if file_hash in all_hashe:
            dublicats.append((str(file),file_size))
            continue
        else:
            all_hashe.append(file_hash)

        if file_ext == ".pdf":
            docs.append(str(file))
        elif file_ext in [".jpg",".png",".jpeg",".jif"]:
            images.append(str(file))
        elif file_ext in [".wav",".mp3",".flac"]:
            audio.append(str(file))
        elif file_ext in [".mp4",".avi",".mov"]:
            video.append(str(file))
        else:
            others.append(str(file))


def image_mover(file):
    shutil.move(str(file),str(target_image))
def doc_mover(file):
    shutil.move(str(file),str(target_doc))
def vedio_mover(file):
   shutil.move(str(file),str(target_vedio))
def other_mover(file):
    shutil.move(str(file),str(target_other))
def audio_mover(file):
    shutil.move(str(file),str(target_audio))
def deleter(file):
    os.remove(file)

if __name__==  "__main__":
    mainn()

    target_image.mkdir(exist_ok=True)
    target_doc.mkdir(exist_ok=True)
    target_vedio.mkdir(exist_ok=True)
    target_audio.mkdir(exist_ok=True)
    target_other.mkdir(exist_ok=True)

    memory_save = sum(item[1] for item in dublicats)/ (1024 * 1024)
    print("\n======= Result =======\n")
    print(f"Image files: {len(images)}\n"
          +f"Vedio files: {len(video)}\n"
          +f"Document files: {len(docs)}\n"
          +f"Audio files: {len(audio)}\n"
          +f"Other Files: {len(others)}\n"
          +f"Duplicates Files: {len(dublicats)}\n"
          +f"Total Memory Saved: {memory_save:.2f}kb\n")
    casee = input("Do You Want to confirm changes? y/n")
    dublicats = [item[0] for item in dublicats]
    if casee.lower() == "y":
        with ThreadPoolExecutor() as ex:
            list(ex.map(image_mover,images))
            list(ex.map(audio_mover,audio))
            list(ex.map(vedio_mover,video))
        with Pool() as pool:
            list(pool.map(doc_mover,docs))
            list(pool.map(other_mover,others))
            list(pool.map(deleter,dublicats))
        print("All Done! ")
    else:
        print("Radhe Radhe")
        
