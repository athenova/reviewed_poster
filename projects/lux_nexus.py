from simple_blogger.blogger.auto.cached import CachedAutoSimpleBlogger
from simple_blogger.poster.telegram import TelegramPoster
from simple_blogger.poster.vk import VkPoster
from simple_blogger.poster.instagram import InstagramPoster
from simple_blogger.preprocessor.text import TagAdder
from simple_blogger.generator.openai import OpenAiTextGenerator, OpenAiImageGenerator
from datetime import date

tagadder = TagAdder(['#гармония', '#светвнутри', '#саморазвитие', '#личностныйрост', '#отношения'])

class LuxNexusBlogger(CachedAutoSimpleBlogger):
    def root_folder(self):
        return f"./files/lux_nexus"
    
    def _path_constructor(self, task):
        return f"{task['category']}/{task['topic']}"
    
    def _message_prompt_constructor(self, task):
        return f"Выбери рандомно актуальную проблему по теме '{task['topic']}' из области '{task['category']}', опиши проблему, выбери рандомно метод решения, опиши метод решения, используй смайлики, используй менее 100 слов"
    
    def _image_prompt_constructor(self, task):
        return f"Нарисуй картинку, вдохновлённую темой '{task['topic']}' из области '{task['category']}'"
    
    def _message_generator(self):
        return OpenAiTextGenerator(self._system_prompt())
    
    def _image_generator(self):
        return OpenAiImageGenerator()
        
    def _posters(self):
        return [
            TelegramPoster(chat_id='@lux_nexus', processor=tagadder),
            VkPoster(group_id='229822258', processor=tagadder),
            InstagramPoster(account_token_name='LUX_NEXUS_TOKEN', processor=tagadder)
        ]

    def __init__(self, posters=None, first_post_date=date(2025, 3, 4), force_rebuild=False):
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
    blogger = LuxNexusBlogger()
    blogger.init_project()

def make_tasks():
    blogger = LuxNexusBlogger()
    blogger.create_auto_tasks()