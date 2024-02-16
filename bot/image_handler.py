import logging
import io
import random
import os
import textwrap
from aiogram import Bot
import aiofiles
from PIL import Image, ImageDraw, ImageFont


class ImageHandler:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def create_image(self, original_user, message, original_user_id):
        try:
            # Retrieve the user's profile photos
            user_photos = await self.bot.get_user_profile_photos(original_user_id, limit=1)

            # Get text from a forwarded message
            if message.reply_to_message and message.reply_to_message.text:
                wrapped_text = textwrap.fill(message.reply_to_message.text, width=23)
            else:
                return  # Exit if the message does not contain text

            # Load default avatar if user has no photo
            avatar_stream = await self._get_avatar_stream(user_photos)

            # Select a random photo from the media folder
            random_photo_path = await self._select_random_photo()
            if not random_photo_path:
                return  # No valid photo files found in the media folder

            # Create the image using the randomly selected photo
            image = Image.open(random_photo_path)
            font_path = os.path.join('media', 'fonts', 'DejaVuSans-BoldOblique.ttf')  # Вкажіть шлях до шрифту
            text_font_size = 90
            info_font_size = 36
            font = ImageFont.truetype(font_path, text_font_size)
            info_font = ImageFont.truetype(font_path, info_font_size)
            draw = ImageDraw.Draw(image)

            # Place a user avatar (round)
            avatar_size = (395, 395)
            avatar = Image.open(avatar_stream)
            avatar = avatar.resize(avatar_size)
            mask = Image.new('L', avatar_size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0) + avatar_size, fill=255)
            image.paste(avatar, (100, 430), mask=mask)

            # Add the message text
            text_position = (1060, 600)
            text_color = (255, 255, 255)
            draw.multiline_text(text_position, wrapped_text, font=font, fill=text_color, anchor="mm", spacing=10)

            # Add information about the user
            username_for_image = f"@{original_user.username}" if original_user.username else "No username"
            info_text = f"Guru: {username_for_image}\nDate: {message.date}"
            info_position = (300, 900)
            draw.text(info_position, info_text, font=info_font, fill=text_color, anchor="mm")

            # Saving images
            output_image = io.BytesIO()
            image.save(output_image, format='PNG')
            output_image.seek(0)

            # Sending an image as a reply to a user's message
            await self.bot.send_photo(message.chat.id, photo=output_image.getvalue(),
                                      reply_to_message_id=message.message_id)
        except Exception as e:
            logging.error(f"Error creating image: {e}")

    async def _get_avatar_stream(self, user_photos):
        if not user_photos or not user_photos.photos:
            logging.info("Using default avatar")
            default_avatar_path = os.path.join('media', 'default-avatar', 'photo_2023-08-26_15-53-15.jpg')
            if os.path.exists(default_avatar_path):
                async with aiofiles.open(default_avatar_path, mode='rb') as file:
                    return io.BytesIO(await file.read())
            else:
                return Image.new('RGB', (395, 395), color='white').tobytes()
        else:
            photo_file_id = user_photos.photos[-1][-1].file_id
            photo_file = await self.bot.get_file(photo_file_id)
            # download file
            avatar_stream = io.BytesIO()
            await photo_file.download(destination_file=avatar_stream)  # download file to BytesIO
            avatar_stream.seek(0)
            return avatar_stream

    @staticmethod
    async def _select_random_photo():
        media_folder = os.path.join('media', 'photo_background')
        photo_filenames = [filename for filename in os.listdir(media_folder) if
                           filename.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if photo_filenames:
            random_photo_filename = random.choice(photo_filenames)
            random_photo_path = os.path.join(media_folder, random_photo_filename)
            return random_photo_path
        else:
            return None
