from simple_blogger.blogger.finite.cached import CachedFiniteSimpleBlogger
from simple_blogger.poster.telegram import TelegramPoster
from simple_blogger.poster.vk import VkPoster
from simple_blogger.preprocessor.text import TagAdder
from simple_blogger.generator.deepseek import DeepSeekTextGenerator
from simple_blogger.generator.yandex import YandexImageGenerator
from datetime import date

tagadder = TagAdder(['#hr', '#кадры', '#it', '#ит', '#айти', '#легенды'])

class LegendaryHrBlogger(CachedFiniteSimpleBlogger):
    def root_folder(self):
        return f"./files/legendary_hr"
    
    def _path_constructor(self, task):
        return f"{task['company']}/{task['name']}"
    
    def _system_prompt(self):
        return 'Ты - руководитель HR, лидер команды со 100% харизмой, всегда оптимистично настроенный и с отличным чувством юмора'
    
    def _message_prompt_constructor(self, task):
        return f"Расскажи интересный факт про '{task['name']}' '{task['position']}' из компании '{task['company']}', используй не более 100 слов, используй смайлики"
    
    def _image_prompt_constructor(self, task):
        return f"Нарисуй рисунок, вдохновлённый '{task['name']}' '{task['position']}' из компании '{task['company']}'"
    
    def _message_generator(self):
        return DeepSeekTextGenerator(self._system_prompt())
    
    def _image_generator(self):
        return YandexImageGenerator()
        
    def _posters(self):
        return [
            TelegramPoster(chat_id='@coffee_and_nerves', processor=tagadder),
            VkPoster(group_id='229838019', processor=tagadder)
        ]

    def __init__(self, posters=None, force_rebuild=False):
        super().__init__(posters=posters or self._posters(), force_rebuild=force_rebuild)

class LegendaryHrReviewer(LegendaryHrBlogger):
    def _check_task(self, task, days_before=1, **_):
        return super()._check_task(task, days_before, **_)
    
def review():
    blogger = LegendaryHrReviewer(
        posters=[TelegramPoster(processor=tagadder)]
    )
    blogger.post()

def post():
    blogger = LegendaryHrBlogger()
    blogger.post()

def init():
    blogger = LegendaryHrBlogger()
    blogger.init_project()

def make_tasks():
    blogger = LegendaryHrBlogger()
    blogger.create_simple_tasks(first_post_date=date(2025, 3, 9), days_between_posts=7)