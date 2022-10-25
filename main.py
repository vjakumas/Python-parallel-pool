from concurrent.futures import ProcessPoolExecutor, as_completed
import cv2
from tqdm import tqdm
from multiprocessing import Pool
from time import time


possible_modes = {
    2: "Single data"
}
data_names = {
    1: "img_250.jpg",
    2: "img_500.jpg",
    3: "img_1000.jpg",
    4: "img_2000.jpg",
    5: "img_3000.jpg",
    6: "img_4000.jpg",
    7: "img_5000.jpg",
    8: "img_6000.jpg"
}


def process_row(row):
    for col in row:
        col[0] = 255 - col[0]
        col[1] = 255 - col[1]
        col[2] = 255 - col[2]
    return row

file_directory = 'C:/Users/viliu/Desktop/lygiagretusIP/'


def main_pool(img_name: str, max_workers: int):
    img_name = ("{0}{1}".format(file_directory,img_name))
    img = cv2.imread(img_name)
    rows, columns, channels = img.shape

    print("\nLygiagretus vykdymas:")
    print(f"plotis(px): {rows}, aukštis(px): {columns}, plotas(px): {rows * columns}")
    progress_bar = tqdm(total=rows * columns)
    start = time()
    with ProcessPoolExecutor(max_workers=max_workers) as worker:
        futures = {worker.submit(process_row, row): count for count, row in enumerate(img)}
        for future in as_completed(futures):
            try:
                count = futures[future]
                progress_bar.update(len(img[count]))
                img[count] = future.result()
            except Exception as er:
                print(f"KLAIDA: {er}")
                progress_bar.close()
    end = time()
    progress_bar.close()
    cv2.imwrite(f"{img_name}-inverted-pool.jpg", img)
    return end - start


def main_single(img_name: str):
    img = cv2.imread("{0}{1}".format(file_directory,img_name))
    rows, columns, channel = img.shape

    print("\nNuoseklus vykdymas:")
    print(f"plotis(px): {rows}, aukštis(px): {columns}, plotas(px): {rows * columns}")
    progress_bar = tqdm(total=rows * columns)
    start = time()
    for row in img:
        for col in row:
            col[0] = 255 - col[0]
            col[1] = 255 - col[1]
            col[2] = 255 - col[2]
            progress_bar.update()
    end = time()
    progress_bar.close()
    cv2.imwrite(f"{img_name}-inverted-single.jpg", img)
    return end - start


def get_wanted_from_dict(possible_values: dict):
    def print_possible_modes():
        print("Pasirinkite nuotraukos numerį:")
        for key, value in possible_values.items():
            print(f"{key}. {value}")
    selected = False
    selection = None
    while not selected:
        print_possible_modes()
        selection = input("Numeris: ")
        try:
            selection = int(selection)
        except Exception:
            print("Įveskite skaičių!")
            continue
        if selection not in possible_values:
            print("Galimi nuotraukų numeriai: ", end="")
            for key in possible_values.keys():
                print(key, end=" ")
            print()
            continue
        else:
            selected = True
    return selection


def run():
    max_workers = get_number_of_workers()
    img = get_wanted_from_dict(data_names)
    img = data_names.get(img)
    time_it_took_pool = main_pool(img, max_workers)
    print(f"Lygiagrečiai užtruko laiko (s): {time_it_took_pool}\n")
    time_it_took_single = main_single(img)
    print(f"\nNuosekliai užtruko laiko (s): {time_it_took_single}")


def get_number_of_workers():
    while True:
        print("\nProcesų skaičius lygiagrečiam vykdymui (nuo 1 iki 10): ")
        num_of_workers = input("Procesai: ")
        try:
            num_of_workers = int(num_of_workers)
        except Exception:
            print("Įveskite skaičiu!")
            continue
        if num_of_workers == None:
            break
        elif num_of_workers < 1 or num_of_workers > 10:
            print("Pasirinkite procesų skaičių nuo 1 iki 10!")
            continue
        max_workers = num_of_workers
        break
    return max_workers


if __name__ == "__main__":
    run()


