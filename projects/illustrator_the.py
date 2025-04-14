from simple_blogger.blogger.finite.cached import CachedFiniteSimpleBlogger
from simple_blogger.poster.telegram import TelegramPoster
from simple_blogger.poster.vk import VkPoster
from simple_blogger.poster.instagram import InstagramPoster
from simple_blogger.preprocessor.text import TagAdder
from simple_blogger.generator.openai import OpenAiTextGenerator, OpenAiImageGenerator
from datetime import date

tagadder = TagAdder(['#иллюстрации', '#книги', '#литература'])

class IllustratorBlogger(CachedFiniteSimpleBlogger):
    def _system_prompt(self):
        return 'Ты - книгоман'
    
    def root_folder(self):
        return f"./files/illustrator_the"
    
    def _path_constructor(self, task):
        return f"{task['author']},{task['book']}/{task['name']}"
    
    def _message_prompt_constructor(self, task):
        return f"Опиши '{task['name']}'({task['description'] if 'description' in task else ''}) из книги '{task['book']}' автора {task['author']}, используй не более 100 слов, используй смайлики"
    
    def _image_prompt_constructor(self, task):
        return f"Нарисуй рисунок, вдохновлённый '{task['name']}'({task['description'] if 'description' in task else ''}) из книги '{task['book']}' автора {task['author']}"
        
    def _message_generator(self):
        return OpenAiTextGenerator(self._system_prompt())
    
    def _image_generator(self):
        return OpenAiImageGenerator()
    
    def _posters(self):
        return [
            TelegramPoster(chat_id='@illustrator_the', processor=tagadder),
            VkPoster(group_id='229821765', processor=tagadder),
            InstagramPoster(account_token_name='ILLUSTRATOR_THE_TOKEN', account_id='9351594524905971', processor=tagadder)
        ]

    def __init__(self, posters=None):
        super().__init__(posters=posters or self._posters())

class IllustratorReviewer(IllustratorBlogger):
    def _check_task(self, task, days_before=1, **_):
        return super()._check_task(task, days_before, **_)

def review():
    blogger = IllustratorReviewer(
        posters=[TelegramPoster(processor=tagadder)]
    )
    blogger.post()

def post():
    blogger = IllustratorBlogger()
    blogger.post()

def print_post():
    blogger = IllustratorReviewer()
    blogger.print_current_task()

def init():
    blogger = IllustratorBlogger()
    blogger.init_project()

def make_tasks():
    blogger = IllustratorBlogger()
    blogger.create_simple_tasks(date(2025, 4, 7))