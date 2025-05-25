from simple_blogger.blogger.finite.cached import CachedFiniteSimpleBlogger
from simple_blogger.poster.telegram import TelegramPoster
from simple_blogger.poster.vk import VkPoster
from simple_blogger.preprocessor.text import TagAdder
from simple_blogger.generator.openai import  OpenAiImageGenerator, OpenAiTextGenerator
from datetime import date

tagadder = TagAdder(['#школа', '#5класс', '#учёба'])

class PupilBlogger(CachedFiniteSimpleBlogger):
    def _system_prompt(self):
        return 'Ты - блогер с 1000000 подписчиков и целевой аудиторией 12 лет, используешь в разговоре сленг и смайлики'
    
    def root_folder(self):
        return f"./files/class5nik"
    
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

    def __init__(self, posters=None, force_rebuild=False, index=None):
        super().__init__(posters or self._posters(), force_rebuild, index)

class PupilReviewer(PupilBlogger):
    def _check_task(self, task, days_before=1, **_):
        return super()._check_task(task, days_before, **_)
    
    def __init__(self, index=None):
        super().__init__([TelegramPoster(processor=tagadder)], True, index)

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

def print_review():
    bloggers = [
        PupilReviewer(),
        PupilReviewer(1),
        PupilReviewer(2),
        PupilReviewer(3),
        PupilReviewer(4),
    ]
    for blogger in bloggers:
        blogger.print_current_task()

def post(index=None):
    blogger = PupilBlogger(index=index)
    blogger.post()

def print_post(index=None):
    blogger = PupilBlogger(index=index)
    blogger.print_current_task()

def init():
    blogger = PupilBlogger()
    blogger.init_project()

def make_tasks():
    blogger = PupilBlogger()
    blogger.create_tasks_between(
        first_post_date=date(2025, 1, 6),
        last_post_date=date(2025, 5, 20),
        multiple_projects=True,
        shuffle=False
    )

# print_post(1)