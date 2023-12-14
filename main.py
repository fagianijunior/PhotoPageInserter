import PySimpleGUI as sg
import os
import json
import functions as f

class Model:
    def __init__(self, name):
        self.name = name
        self.data_file = f"./models/{name}/data.json"
        self.pages = self.load_pages()

    def load_pages(self):
        with open(self.data_file, "r") as file:
            model_data = json.load(file)
            return model_data.get("pages", [])
    
    def get_page_filename(self, page_number):
        with open(self.data_file, "r") as file:
            model_data = json.load(file)
            if "pages" in model_data and isinstance(model_data["pages"], list):
                return len(model_data["pages"])
            return 0

def main():
    models_dir = next(os.walk("./models/"))[1]
    photos_dir = "./photos/"

    layout = [
        [sg.Text("Select the model:"), sg.Combo(models_dir, enable_events=True, key="-COMBOMODELS-")],
        [sg.Text("Select photos dir:")],
        [sg.FolderBrowse(key="-FOLDERPHOTOS-", initial_folder='photos'), sg.Text("")],
        [sg.Checkbox("Repetir foto", key="-SAMEPHOTO-")],
        [sg.Button("Gerar")]
    ]

    window = sg.Window("PySimpleGUI Example").layout(layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == "-COMBOMODELS-":
            selected_model = values["-COMBOMODELS-"]
        elif event == "Gerar":
            if selected_model:
                model = Model(selected_model)
                f.generate_calendar(model=model, photos_dir=values["-FOLDERPHOTOS-"], same_photo=values["-SAMEPHOTO-"])


    window.close()

if __name__ == "__main__":
    main()