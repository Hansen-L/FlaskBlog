from flaskblog.models import User, Post, Images
from flaskblog import bcrypt, db
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flaskblog.gallery.utils import save_picture, delete_picture, save_zip, share_email
from flaskblog.gallery.forms import UploadPictureForm, SearchForm, DeleteSubmit, ShareForm
from flask_login import current_user, login_required
import os
from sqlalchemy import or_

gallery = Blueprint('gallery', __name__)  # Configuring


@gallery.route("/gallery/upload", methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadPictureForm()
    if form.validate_on_submit():
        description = form.description.data
        if form.pictures.data:
            for file in form.pictures.data:
                f_ext = os.path.splitext(file.filename)[1]  # Get the extension of the uploaded file
                if f_ext == '.zip':
                    save_zip(file, description, current_user)
                else:  # If the files are png or jpg
                    save_picture(file, description, current_user, assign_google_labels=True)  # Saves the picture to the server and returns the filepath
            db.session.commit()
            flash('Image(s) uploaded!', 'success')
        return redirect(url_for('gallery.upload'))
    return render_template('upload.html', title='Upload Images', form=form)


@gallery.route("/gallery/<file_id>/delete")
@login_required
def delete(file_id):
    image = Images.query.get_or_404(file_id)
    if image.author != current_user:
        abort(403)
    delete_picture(file_id)
    db.session.commit()
    flash('Your image has been deleted!', 'success')
    return redirect(url_for('gallery.user_gallery'))


@gallery.route("/gallery/delete/all")
@login_required
def delete_all():
    images = Images.query.filter_by(author=current_user).order_by(Images.id.desc())
    if images[0].author != current_user:
        abort(403)
    if images:
        for image in images:
            delete_picture(image.id)
        db.session.commit()
        flash('All images have been deleted!', 'success')
    return redirect(url_for('gallery.user_gallery'))


@gallery.route("/gallery", methods=['GET', 'POST'])
def image_gallery():
    search_form = SearchForm()
    share_form = ShareForm()
    if share_form.submit.data:  # Clicking on "Share Selected Pictures" button
        images = []
        if request.form.getlist("images"):
            for image_id in request.form.getlist("images"):  # Gather images we want to share
                images.append(Images.query.get(image_id))
            share_email(share_form.recipient_email.data, images)
            flash('Your images have been sent!', 'success')
    if search_form.search.data:  # If we are searching the gallery
        images = Images.query.filter(or_(Images.description.contains(search_form.search.data), Images.google_labels.contains(search_form.search.data))).order_by(Images.id.desc()).all()
    else:
        images = Images.query.order_by(Images.id.desc()).all()  # If we don't have a search form, refresh the database after deleting the images
    return render_template('gallery.html', images=images, form=search_form, share_form=share_form)


@gallery.route("/gallery/user_gallery", methods=['GET', 'POST'])
@login_required
def user_gallery():
    search_form = SearchForm()
    deletesubmit = DeleteSubmit()  # Form to detect when we click "Delete selection" button
    if deletesubmit.submit.data:  # If we click "Delete selection"
        if request.form.getlist("images"):  # If we select images for deletion
            for image_id in request.form.getlist("images"):
                delete_picture(image_id)
            db.session.commit()
    if search_form.search.data:  # If we are searching the gallery
        images = Images.query.filter(or_(Images.description.contains(search_form.search.data), Images.google_labels.contains(search_form.search.data))).filter_by(author=current_user).order_by(Images.id.desc()).all()
    else:
        images = Images.query.filter_by(author=current_user).order_by(Images.id.desc()).all()  # If we don't have a search form, refresh the database after deleting the images
    return render_template('user_gallery.html', images=images, form=search_form, deletesubmit=deletesubmit)


