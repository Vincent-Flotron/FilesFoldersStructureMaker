# Folder and File Structure Maker

This script provides a Gui to create a folder and file structure based (often generate by ChatGPT) on a given text representation. The structure is created at the specified root folder path.

## Main function: `make`

### Description

The `make` function creates the folders and files structure at the specified `root_folder_path` location, following the structure defined in `structure_text`.

### Parameters

- `root_folder_path` (str): The root directory where the structure will be created.
- `structure_text` (str): A string representing the folder and file structure to be created.

### Example

```python
root_folder_path = '/home/me/root_folder'
structure_text = """
folders_and_files_structure_demo/
├── static/
│   ├── css/
│   ├── js/
├── templates/
├── app.py
├── models.py
└── database.db
"""