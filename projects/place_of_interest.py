from simple_blogger.blogger.auto import AutoBlogger
from simple_blogger.poster.telegram import TelegramPoster
from simple_blogger.poster.vk import VkPoster
from simple_blogger.poster.instagram import InstagramPoster
from simple_blogger.editor import Editor
from simple_blogger.preprocessor.text import TagAdder
from simple_blogger.generator.openai import OpenAiTextGenerator, OpenAiImageGenerator
from datetime import date

tagadder = TagAdder(['#путешествия', '#достопримечательности', '#города', '#страны'])
first_post_date=date(2025, 2, 23)
root_folder = f"./files/place_of_interest"

class LuxNexusBlogger(AutoBlogger):
    def root_folder(self):
        return root_folder
    
    def _path_constructor(self, task):
        return f"{task['country']}/{task['name']}"
    
    def _system_prompt(self):
        return f"Ты - блогер с 1000000 миллионном подписчиков"
    
    def _message_prompt_constructor(self, task):
        return f"Расскажи интересный факт про {task['name']}, который находятся в {task['location']} {task['country']}, используй не более 100 слов, используй смайлики"
    
    def _image_prompt_constructor(self, task):
        return f"Нарисуй {task['name']}, который находятся в {task['location']} {task['country']}"
    
    def _message_generator(self):
        return OpenAiTextGenerator(self._system_prompt())
    
    def _image_generator(self):
        return OpenAiImageGenerator()
        
    def _posters(self):
        return [
            TelegramPoster(chat_id='@place_of_interest', processor=tagadder),
            VkPoster(group_id='229821893', processor=tagadder),
            InstagramPoster(account_token_name='PLACE_OF_INTEREST_THE_TOKEN', processor=tagadder)
        ]

    def __init__(self, posters=None, first_post_date=first_post_date, force_rebuild=False):
        super().__init__(posters=posters or self._posters(), first_post_date=first_post_date, force_rebuild=force_rebuild)

class LuxNexusReviewer(LuxNexusBlogger):
    def _check_task(self, task, tasks, days_before=1):
        return super()._check_task(task, tasks, days_before)
    
def review():
    blogger = LuxNexusReviewer(
        posters=[TelegramPoster(processor=tagadder)],
        force_rebuild=True
    )
    blogger.post()

def post():
    blogger = LuxNexusBlogger()
    blogger.post()

def init():
    editor = Editor(root_folder)
    editor.init_project()

def make_tasks():
    editor = Editor(root_folder)
    editor.create_auto(day_offset=-53)
