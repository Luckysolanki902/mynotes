import os
import glob
from bs4 import BeautifulSoup
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def get_next_image_name():
    current_files = glob.glob('images/staticLoading/image*.png') + glob.glob('images/staticLoading/image*.jpg')
    return f"image{len(current_files) + 1}.png"

def add_image_to_html(file_name):
    html_file = './unit2_1.html'

    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')

        main_div = soup.find('main')
        new_div = soup.new_tag('div')
        img_tag = soup.new_tag('img', src=f"images/staticLoading/{file_name}", style="width: 100%;", alt="")
        new_div.append(img_tag)
        main_div.append(new_div)

    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))

def append_image_to_html(file_name):
    html_file = './unit2_1.html'

    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')

        main_div = soup.find('main')
        new_div = soup.new_tag('div')
        img_tag = soup.new_tag('img', src=f"images/staticLoading/{file_name}", style="width: 100%;", alt="")
        new_div.append(img_tag)

        # Append the new div with the image tag to the end of the main tag
        main_div.append(new_div)

    with open(html_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(('.png', '.jpg')):
            try:
                new_name = get_next_image_name()
                os.rename(os.path.normpath(event.src_path), os.path.normpath(f"images/staticLoading/{new_name}"))
                print(f"Renamed {event.src_path} to {new_name}")
                append_image_to_html(new_name)
                print(f"Added {new_name} to HTML.")
                print("Watching for changes in the folder...")
            except Exception as e:
                print(f"Error processing {event.src_path}: {e}")

def watch_folder():
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='D:/Desktop/notes/images/staticLoading', recursive=False)
    print("Watching for changes in the folder...")
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    watch_folder()
