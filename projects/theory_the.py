from simple_blogger.blogger.finite.cached  import CachedFiniteSimpleBlogger
from simple_blogger.poster.telegram import TelegramPoster
from simple_blogger.poster.vk import VkPoster
from simple_blogger.poster.instagram import InstagramPoster
from simple_blogger.preprocessor.text import TagAdder
from simple_blogger.generator.openai import OpenAiTextGenerator, OpenAiImageGenerator
from datetime import date

tagadder = TagAdder(['#интересныетеории', '#теории'])

class TheoristBlogger(CachedFiniteSimpleBlogger):
    def root_folder(self):
        return f"./files/theory_the"
    
    def _path_constructor(self, task):
        return f"{task['domain']},{task['category']}/{task['name']}"
    
    def _message_prompt_constructor(self, task):
        return f"Расскажи интересный факт про теорию '{task['name']}' из категории '{task['category']}' из области '{task['domain']}', используй не более 100 слов, используй смайлики"
    
    def _image_prompt_constructor(self, task):
        return f"Нарисуй рисунок, вдохновлённый теорией '{task['name']}' из категории '{task['category']}' из области '{task['domain']}'"
        
    def _message_generator(self):
        return OpenAiTextGenerator(self._system_prompt())
    
    def _image_generator(self):
        return OpenAiImageGenerator()
    
    def _posters(self):
        return [
            TelegramPoster(chat_id='@theory_the', processor=tagadder),
            VkPoster(group_id='229822056', processor=tagadder),
            InstagramPoster(account_token_name='IN_THEORY_THE_TOKEN', account_id='9431105350315600', processor=tagadder)
        ]

    def __init__(self, posters=None):
        super().__init__(posters=posters or self._posters())

class TheoristReviewer(TheoristBlogger):
    def _check_task(self, task, days_before=1, **_):
        return super()._check_task(task, days_before, **_)

def review():
    blogger = TheoristReviewer(
        posters=[TelegramPoster(processor=tagadder)]
    )
    blogger.post()

def post():
    blogger = TheoristBlogger()
    blogger.post()

def init():
    blogger = TheoristBlogger()
    blogger.init_project()

def make_tasks():
    blogger = TheoristBlogger()
    blogger.create_simple_tasks(first_post_date=date(2025, 4, 7))