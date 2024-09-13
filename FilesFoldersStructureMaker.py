import regex as re
import os


class FilesFoldersStructureMaker:
    # To locate the actual folder path
    folder_stack = []
    root_depth   = 0

    # Regex
    location_pattern = re.compile( r"(?:│\s{2})|(?:├──)|(?:└──)" )
    folder_pattern   = re.compile( r"\b[\p{L}._-]+(?=\s*/$)"     )
    file_pattern     = re.compile( r"\b([\p{L}._-]+)\s*(?!/)$"   )
    empty_line       = re.compile( r"^$")

    def _reset_location():
        global root_depth  # Because editing the variable's value here
        FilesFoldersStructureMaker.folder_stack.clear()
        FilesFoldersStructureMaker.root_depth = 0

    def _add_root_to_folder_stack( root_folder ):
        """Adding the root_folder to the 'folder_stack'."""
        global root_depth  # Because editing the variable's value here
        for folder in root_folder.split( "/" ):
            if folder != '':
                FilesFoldersStructureMaker.folder_stack.append( folder )
                FilesFoldersStructureMaker.root_depth += 1

    def _get_actual_folder( depth ):
        """Get the actual folder's path regarding at the difference between the number of 'folder_stack' and the 'depth'."""
        # Update the folder_stack
        for i in range( len( FilesFoldersStructureMaker.folder_stack ) - depth ):
            FilesFoldersStructureMaker.folder_stack.pop()
        # Update the actual_folder_path
        actual_folder_path = "/" + "/".join( FilesFoldersStructureMaker.folder_stack )
        # Set default path to '/' None
        if len( FilesFoldersStructureMaker.folder_stack ) == 0:
            actual_folder_path = "/"
        return actual_folder_path

    def _create_empty_file( file_path ):
        """Create an empty file if not already existing."""
        if not os.path.exists( file_path ):
            with open( file_path, 'w' ) as f:
                    f.write( '' )             # Create an empty file

    def make( root_folder_path, structure_text ):
        """Make the folders and files structure at the 'root_folder_path' location and following the 'structure_text'.
        Example:
            root_folder_path = '/home/me/root_folder'
            structure_text   = 
           'under_control/
            ├── static/
            │   ├── css/
            │   ├── js/
            ├── templates/
            ├── app.py
            ├── models.py
            └── database.db'
        """
        FilesFoldersStructureMaker._reset_location()
        FilesFoldersStructureMaker._add_root_to_folder_stack( root_folder_path )
        depth = 0

        for l in structure_text.splitlines():
            # Skip empty lines
            if re.match( FilesFoldersStructureMaker.empty_line, l ):
                continue

            # Catch folder, file or location info: "│  " "├──" "└──"
            where_matches  = re.findall( FilesFoldersStructureMaker.location_pattern, l)
            folder_to_make = re.search(  FilesFoldersStructureMaker.folder_pattern,   l)
            file_to_make   = re.search(  FilesFoldersStructureMaker.file_pattern,     l)

            # Get the actual folder
            depth              = FilesFoldersStructureMaker.root_depth + len( where_matches )
            actual_folder_path = FilesFoldersStructureMaker._get_actual_folder( depth )

            # Create folder or empty file
            if folder_to_make:
                # Set the folder's path to make
                folder_to_make     = folder_to_make.group()
                actual_folder_path = os.path.join( actual_folder_path, folder_to_make )
                # Make the folder
                try:
                    os.makedirs( actual_folder_path, exist_ok=True )
                except Exception as e:
                    return e
                # Update the folder stack with the latest created folder
                FilesFoldersStructureMaker.folder_stack.append( folder_to_make )
            elif file_to_make:
                # Set the folder's path to make
                file_to_make     = file_to_make.group()
                actual_file_path = os.path.join( actual_folder_path, file_to_make )
                # Make the empty file
                try:
                    FilesFoldersStructureMaker._create_empty_file( actual_file_path )
                except Exception as e:
                    return e


if __name__ == "__main__":
    # Example usage
    text = """
    under_control/
    ├── static/
    │   ├── css/
    │   ├── js/
    ├── templates/
    ├── app.py
    ├── models.py
    └── database.db
    """

    text = """
    under_control/
    ├── static/
    │   ├── css/
    │   │   ├── base/
    │   │   │   ├── reset.css
    │   │   │   ├── styles.css
    │   │   ├── theme/
    │   │   │   ├── dark.css
    │   │   │   ├── light.css
    │   ├── js/
    │   │   ├── modules/
    │   │   │   ├── app.js
    │   │   │   ├── service.js
    │   │   ├── vendor/
    │   │   │   ├── jquery.js
    │   │   │   ├── bootstrap.js
    ├── templates/
    │   ├── layouts/
    │   │   ├── header.html
    │   │   ├── footer.html
    │   ├── includes/
    │   │   ├── navbar.html
    │   │   ├── sidebar.html
    │   ├── pages/
    │   │   ├── home.html
    │   │   ├── about.html
    ├── app.py
    ├── models.py
    └── database.db
    """

    FilesFoldersStructureMaker.make( '/home/me/Documents/git/FilesFoldersStructureMaker', text )