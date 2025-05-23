from simple_blogger.blogger.finite.cached import CachedFiniteSimpleBlogger
from simple_blogger.poster.telegram import TelegramPoster
from simple_blogger.poster.vk import VkPoster
from simple_blogger.poster.instagram import InstagramPoster
from simple_blogger.preprocessor.text import TagAdder
from simple_blogger.generator.deepseek import DeepSeekTextGenerator
from simple_blogger.generator.yandex import YandexImageGenerator
from datetime import date

tagadder = TagAdder(['#гармония', '#светвнутри', '#легенды'])

class LegendaryAwakenBlogger(CachedFiniteSimpleBlogger):
    def root_folder(self):
        return f"./files/legendary_awaken"
    
    def _path_constructor(self, task):
        return f"{task['country']}/{task['name']}"
    
    def _message_prompt_constructor(self, task):
        return f"Расскажи интересный факт про '{task['name']}' из '{task['country']}', используй не более 100 слов, используй смайлики"
    
    def _image_prompt_constructor(self, task):
        return f"Нарисуй рисунок, вдохновлённый '{task['name']}' из '{task['country']}'"
    
    def _message_generator(self):
        return DeepSeekTextGenerator(self._system_prompt())
    
    def _image_generator(self):
        return YandexImageGenerator()
        
    def _posters(self):
        return [
            TelegramPoster(chat_id='@lux_nexus', processor=tagadder),
            VkPoster(group_id='229822258', processor=tagadder),
            InstagramPoster(account_token_name='LUX_NEXUS_TOKEN', processor=tagadder)
        ]

    def __init__(self, posters=None, force_rebuild=False):
        super().__init__(posters=posters or self._posters(), force_rebuild=force_rebuild)

class LegendaryAwakenReviewer(LegendaryAwakenBlogger):
    def _check_task(self, task, days_before=1, **_):
        return super()._check_task(task, days_before, **_)

def review():
    blogger = LegendaryAwakenReviewer(
        posters=[TelegramPoster(processor=tagadder)]
    )
    blogger.post()

def post():
    blogger = LegendaryAwakenBlogger()
    blogger.post()

def init():
    blogger = LegendaryAwakenBlogger()
    blogger.init_project()

def make_tasks():
    blogger = LegendaryAwakenBlogger()
    blogger.create_simple_tasks(first_post_date=date(2025, 3, 9), days_between_posts=7)