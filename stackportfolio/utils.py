import cloudinary.uploader


def upload_to_cloudinary(image):
    """
    Handles the formatting of profile images in Cloudinary.
    """
    response = cloudinary.uploader.upload(
        image,
        format='webp',
        transformation=[
            {'width': 300, 'crop': 'limit'},
            {'quality': 90}
        ]
    )

    return response['url'], response['public_id']


def upload_project_to_cloudinary(image):
    """
    Handles the formatting of project images in Cloudinary.
    """
    response = cloudinary.uploader.upload(
        image,
        format='webp',
        transformation=[
            {'width': 1500, 'crop': 'limit'},
            {'quality': 95}
        ]
    )

    return response['url'], response['public_id']
