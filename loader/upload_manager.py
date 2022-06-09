import logging
import os
import random

from loader.exceptions import PictureFormatNotSupportedError, PictureNotUploadedError, OutOfFreeNamesError

logger = logging.getLogger("basic")

class UploadManager:

    def get_free_filename(self, folder, file_type):

        attemps = 0
        RANGE_OF_IMAGE_NUMBERS = 5
        LIMIT_OF_ATTEMPS = 1000

        while True:
            pic_name = str(random.randint(0, RANGE_OF_IMAGE_NUMBERS))
            filename_to_save = f"{pic_name}.{file_type}"
            os_path = os.path.join(folder, filename_to_save)
            is_filename_occupied = os.path.exists(os_path)

            if not is_filename_occupied:
                return filename_to_save

            attemps += 1

            if attemps > LIMIT_OF_ATTEMPS:
                logger.info(f"ERROR: файл не загружен. достигнут лимит загрузок")
                raise OutOfFreeNamesError('Нет свободных имен для сохранения изображения')

    def is_file_type_valid(self ,file_type):

        if file_type.lower() in ["jpg", "jpeg", "gif", "png", "webp", "tif"]:
            return True
        return False

    def save_with_random_name(self, picture):
        # Получаем данные с картинки
        filename = picture.filename
        file_type = filename.split('.')[-1]

        # Проверяем валидность картинки
        if not self.is_file_type_valid(file_type):
            logger.info(f"Ошибка загрузки файла. Загружаемый файл не является картинкой")
            raise PictureFormatNotSupportedError(f"Форамат {file_type} не поддерживается")

        # Получаем свободное имя
        folder = os.path.join(".", "uploads", "images")
        filename_to_save = self.get_free_filename(folder, file_type)

        # Сохраняем под новым именем
        try:
            picture.save(os.path.join(folder, filename_to_save))
        except FileNotFoundError:
            raise PictureNotUploadedError(f"{folder, filename_to_save}")

        return filename_to_save

