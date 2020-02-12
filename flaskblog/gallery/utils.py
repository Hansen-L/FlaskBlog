from flask import url_for, current_app
from PIL import Image
import secrets, os
from flaskblog.models import Images
from flaskblog import db
from zipfile import ZipFile
from shutil import rmtree
from werkzeug.datastructures import FileStorage

def save_picture(picture, description, author):
    # Add a single picture to the server and the db. Commit the db after running this function.
    # Input is a FileStorage object

    random_hex = secrets.token_hex(8)
    f_ext = os.path.splitext(picture.filename)[1]  # Get the extention from the picture
    picture_fn = random_hex + f_ext  # Rename the picture with a random hex
    picture_path = os.path.join(current_app.root_path, 'static/gallery_images', picture_fn)

    output_size = (500, 500)  # Save the image as 300px wide while preserving aspect ratio
    i = Image.open(picture)
    i.thumbnail(output_size)

    i.save(picture_path)  # Save the image to the static/images directory on the server

    image = Images(image_file=picture_fn, description=description, author=author)
    db.session.add(image)
    return picture_fn


def save_pictures_zip(file, description, author):
    valid_images = [".jpg", ".png"]
    temp_path = os.path.join(current_app.root_path,'static/gallery_images/temp')
    zip_path = os.path.join(current_app.root_path, 'static/gallery_images', file.filename)
    file.save(zip_path)  # Save the zip temporarily
    with ZipFile(zip_path, "r") as zipObj:
        zipObj.extractall(temp_path)  # Extract the pictures. We will reformat them and rename them before deleting the originals.

    for file_name in os.listdir(temp_path):
        f_ext = os.path.splitext(file_name)[1]
        if f_ext.lower() not in valid_images:  # Ignore files that are not .jpg or .png
            continue
        else:
            with open(os.path.join(temp_path, file_name), 'rb') as picture:
                picture_fs = FileStorage(picture)  # Wrapping the file into the FileStorage class
                save_picture(picture_fs, description, author=author)

    os.remove(zip_path)  # Getting rid of temp files
    print(rmtree(temp_path))


def delete_picture(image_id):
    # Delete a single picture from the server and the db. Commit the db after running this function.
    image = Images.query.get_or_404(image_id)
    filepath = url_for('static', filename='gallery_images/' + image.image_file)
    filepath = os.getcwd() + '/flaskblog/' + filepath  # Get picture's location on the server
    os.remove(filepath)  # Remove picture from the server
    db.session.delete(image)  # Update the database. Commit after deleting all required images