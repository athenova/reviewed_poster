from simple_blogger.blogger.finite.cached import CachedFiniteSimpleBlogger
from simple_blogger.poster.telegram import TelegramPoster
from simple_blogger.poster.vk import VkPoster
from simple_blogger.poster.instagram import InstagramPoster
from simple_blogger.preprocessor.text import TagAdder
from simple_blogger.generator.openai import OpenAiTextGenerator, OpenAiImageGenerator
from datetime import date

tagadder = TagAdder(['#меломан', '#музыка', '#рок', '#иллюстрации', '#песни' ])

class MelomanBlogger(CachedFiniteSimpleBlogger):
    def root_folder(self):
        return f"./files/meloman_the"
    
    def _path_constructor(self, task):
        return f"{task['group']},{task['album']}/{task['song']}"
    
    def _message_prompt_constructor(self, task):
        return f"Расскажи про песню '{task['song']}' c альбома '{task['album']}' группы '{task['group']}', используй не более 100 слов, используй смайлики"
    
    def _image_prompt_constructor(self, task):
        return f"Нарисуй рисунок, вдохновлённый песней '{task['song']}' c альбома '{task['album']}' группы '{task['group']}'"
        
    def _message_generator(self):
        return OpenAiTextGenerator(self._system_prompt())
    
    def _image_generator(self):
        return OpenAiImageGenerator()
    
    def _posters(self):
        return [
            TelegramPoster(chat_id='@meloman_the', processor=tagadder),
            VkPoster(group_id='229821806', processor=tagadder),
            InstagramPoster(account_token_name='MELOMAN_THE_TOKEN', account_id='28744401475175260', processor=tagadder)
        ]

    def __init__(self, posters=None):
        super().__init__(posters=posters or self._posters())

class MelomanReviewer(MelomanBlogger):
    def _check_task(self, task, days_before=1, **_):
        return super()._check_task(task, days_before, **_)

def review():
    blogger = MelomanReviewer(
        posters=[TelegramPoster(processor=tagadder)]
    )
    blogger.post()

def post():
    blogger = MelomanBlogger()
    blogger.post()

def init():
    blogger = MelomanBlogger()
    blogger.init_project()

def make_tasks():
    blogger = MelomanBlogger()
    blogger.create_simple_tasks(first_post_date=date(2025, 4, 7))
