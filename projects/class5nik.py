from simple_blogger.blogger.basic import SimpleBlogger
from simple_blogger.poster.telegram import TelegramPoster
from simple_blogger.poster.vk import VkPoster
from simple_blogger.editor import Editor
from simple_blogger.preprocessor.text import TagAdder
from simple_blogger.generator.openai import  OpenAiImageGenerator, OpenAiTextGenerator
from datetime import date

tagadder = TagAdder(['#школа', '#5класс', '#учёба'])
root_folder = f"./files/class5nik"

class PupilBlogger(SimpleBlogger):
    def _system_prompt(self):
        return 'Ты - блогер с 1000000 подписчиков и целевой аудиторией 12 лет, используешь в разговоре сленг и смайлики'
    
    def root_folder(self):
        return root_folder
    
    def _path_constructor(self, task):
        return f"{task['category']}/{task['topic']}"
    
    def _message_prompt_constructor(self, task):
        topic = f"{task['author']}. {task['topic']}" if 'author' in task else task['topic']
        return f"Напиши интересный факт по теме '{topic}' из '{task['category']}', используй менее 200 слов"
    
    def _image_prompt_constructor(self, task):
        topic = f"{task['author']}. {task['topic']}" if 'author' in task else task['topic']
        return f"Нарисуй картинку, вдохновлённую темой '{topic}' из '{task['category']}'"
        
    def _message_generator(self):
        return OpenAiTextGenerator(self._system_prompt())

    def _image_generator(self):
        return OpenAiImageGenerator()
    
    def _posters(self):
        return [
            TelegramPoster(chat_id='@class5nik', processor=tagadder),
            VkPoster(group_id='229821544', processor=tagadder)
        ]

    def __init__(self, posters=None, index=None):
        super().__init__(posters=posters or self._posters(),index=index)

class PupilReviewer(PupilBlogger):
    def _check_task(self, task, days_before=1, **_):
        return super()._check_task(task, days_before, **_)
    
    def __init__(self, index=None):
        super().__init__([TelegramPoster(processor=tagadder)], index)

def review():
    bloggers = [
        PupilReviewer(),
        PupilReviewer(1),
        PupilReviewer(2),
        PupilReviewer(3),
        PupilReviewer(4),
    ]
    for blogger in bloggers:
        blogger.post()

def post(index=None):
    blogger = PupilBlogger(index=index)
    blogger.post()

def init():
    editor = Editor(root_folder,multiple_projects=True,shuffle_tasks=False)
    editor.init_project()

def make_tasks():
    editor = Editor(root_folder,multiple_projects=True,shuffle_tasks=False)
    first_post_date=date(2025, 1, 6)
    last_post_date=date(2025, 5, 20)
    editor.create_between(first_post_date=first_post_date, last_post_date=last_post_date)