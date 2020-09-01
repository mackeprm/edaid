# TODO upsert image (only insert if PATH is not in the db, otherwise, update metadata)
# TODO sorting of duplicates
# TODO handling of duplicates
from send2trash import send2trash


class DuplicateService:
    def __init__(self, image_repository):
        self.image_repository = image_repository

    def upsert(self, image_info):
        if self.image_repository.find_by_path(image_info['path']):
            self.image_repository.update(image_info)
        else:
            self.image_repository.save(image_info)

    def delete(self, id, path):
        send2trash(path)
        self.image_repository.remove_by_id(id)
