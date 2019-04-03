from . import database
from .models import Category, Content, ContentMetadatum, User
import datetime
import mistune

class View:
    def __init__(self, category_name, body, markdown_content, title, last_edited, last_edited_by, tags, metadata = None):
        self.category_name = category_name
        self.body = body
        self.markdown_content = markdown_content
        self.title = title
        self.last_edited = last_edited
        self.last_edited_by = last_edited_by
        self.tags = tags
        self.metadata = metadata


def create_view_from_db(uri_subs):
    try:
        category_name = '+'.join(uri_subs)
        category = Category.query.filter_by(category_name=category_name).first()
        content_id = category.content_id
        content = Content.query.filter_by(content_id=content_id).first()
        content_metadata = ContentMetadatum.query.filter_by(metadata_id=content.content_metadata_id).first()
        owner = User.query.filter_by(user_id=content.owner_id).first()
        return View(
            category_name = category_name,
            body = convert_markdown_to_html(content.data),
            markdown_content = content.data,
            title = content.title,
            last_edited = content.last_edited,
            last_edited_by = content.last_edited_by,
            tags = []
        )
    except:
        pass
    finally:
        pass


def persist_view_into_db(view):
    try:
        category_instance = Category.query.filter_by(category_name=view.category_name).first()

        # Resolve on existing category.
        if category_instance:
            existing_content = Content.query.filter_by(content_id=category_instance.content_id).first()
            existing_content.data = view.markdown_content
            existing_content.title = view.title
            existing_content.last_edited_by = view.last_edited_by
            existing_content.last_edited = view.last_edited
        # Create new content and category.
        else:
            content = Content(
                title = view.title,
                data = view.markdown_content,
                last_edited_by = view.last_edited_by,
                last_edited = datetime.datetime.now(),
                owner_id = 1,  # Need correct value
                tag_id = 1,    # Need correct value
                content_metadata_id = 1,    # Need correct value
            )

            database.session.add(content)
            database.session.flush()

            category = Category(
                category_name = view.category_name,
                content_id = content.content_id,
                parent_id = 0
            )

            database.session.add(category)
    finally:
        pass


def delete_view_from_db(category_name):
    try:
        category_instance = Category.query.filter_by(category_name=category_name).first()

        # Resolve on existing category.
        if category_instance:
            existing_content = Content.query.filter_by(content_id=category_instance.content_id).first()
            database.session.delete(existing_content)
    finally:
        database.session.delete(category_instance)
        pass


def convert_markdown_to_html(data):
    body_html = mistune.markdown(data)
    return body_html


# TODO: Create parent category if not existing.
def get_parent_category(category_name):
    # The category name is defined as parent+child+grandchild...
    parent_category_name = '+'.join(category_name.split('+')[:-1])
    category_instance = Category.query.filter_by(category_name=parent_category_name).first()

    return category_instance