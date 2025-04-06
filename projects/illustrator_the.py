from simple_blogger.blogger.basic import SimpleBlogger
from simple_blogger.poster.TelegramPoster import TelegramPoster
from simple_blogger.poster.VkPoster import VkPoster
from simple_blogger.poster.InstagramPoster import InstagramPoster
from simple_blogger.editor import Editor
from simple_blogger.preprocessor.text import TagAdder
from simple_blogger.generator.openai import OpenAiTextGenerator, OpenAiImageGenerator
from datetime import date

tagadder = TagAdder(['#иллюстрации', '#книги', '#литература'])
root_folder = f"./files/illustrator_the"

class IllustratorBlogger(SimpleBlogger):
    def _system_prompt(self):
        return 'Ты - книгоман'
    
    def root_folder(self):
        return root_folder
    
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

def init():
    editor = Editor(root_folder)
    editor.init_project()

def make_tasks():
    editor = Editor(root_folder)
    first_post_date=date(2025, 4, 7)
    editor.create_simple(first_post_date=first_post_date)