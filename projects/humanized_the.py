from simple_blogger.blogger.basic import SimpleBlogger
from simple_blogger.poster.telegram import TelegramPoster
from simple_blogger.poster.vk import VkPoster
from simple_blogger.poster.instagram import InstagramPoster
from simple_blogger.editor import Editor
from simple_blogger.preprocessor.text import TagAdder
from simple_blogger.generator.openai import OpenAiTextGenerator, OpenAiImageGenerator
from datetime import date

tagadder = TagAdder(['#иллюстрации', '#фантазии'])
root_folder = f"./files/humanized_the"

class HumanizedBlogger(SimpleBlogger):
    def _system_prompt(self):
        return 'Ты - художник с образованием психолога'
    
    def root_folder(self):
        return root_folder
    
    def _path_constructor(self, task):
        return f"{task['group']}/{task['name']}"
    
    def _message_prompt_constructor(self, task):
        return f"Опиши, как бы выглядел {task['group']} '{task['name']}', если бы был человеком, используй не более 100 слов, используй смайлики"
    
    def _image_prompt_constructor(self, task):
        return f"Нарисуй, как бы выглядел {task['group']} '{task['name']}', если бы был человеком"
        
    def _message_generator(self):
        return OpenAiTextGenerator(self._system_prompt())
    
    def _image_generator(self):
        return OpenAiImageGenerator()
    
    def _posters(self):
        return [
            TelegramPoster(chat_id='@humanized_the', processor=tagadder),
            VkPoster(group_id='229862079', processor=tagadder),
            InstagramPoster(account_token_name='HUMANIZED_THE_TOKEN', account_id='9396881250388941', processor=tagadder)
        ]

    def __init__(self, posters=None):
        super().__init__(posters=posters or self._posters())

class HumanizedReviewer(HumanizedBlogger):
    def _check_task(self, task, days_before=1, **_):
        return super()._check_task(task, days_before, **_)

def review():
    blogger = HumanizedReviewer(
        posters=[TelegramPoster(processor=tagadder)]
    )
    blogger.post()

def post():
    blogger = HumanizedBlogger()
    blogger.post()

def init():
    editor = Editor(root_folder)
    editor.init_project()

def make_tasks():
    editor = Editor(root_folder)
    first_post_date=date(2025, 3, 26)
    editor.create_simple(first_post_date=first_post_date)