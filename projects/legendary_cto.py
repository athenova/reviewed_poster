from simple_blogger.blogger.basic import SimpleBlogger
from simple_blogger.poster.TelegramPoster import TelegramPoster
from simple_blogger.poster.VkPoster import VkPoster
from simple_blogger.editor import Editor
from simple_blogger.preprocessor.text import TagAdder
from simple_blogger.generator.deepseek import DeepSeekTextGenerator
from simple_blogger.generator.yandex import YandexImageGenerator
from datetime import date

tagadder = TagAdder(['#cto', '#it', '#ит', '#айти', '#легенды'])
root_folder = f"./files/legendary_cto_in"

class LegendaryCtoBlogger(SimpleBlogger):
    def root_folder(self):
        return root_folder
    
    def _path_constructor(self, task):
        return f"{task['company']}/{task['name']}"
    
    def _system_prompt(self):
        return f"Ты - технический директор, лидер команды со 100% харизмой, всегда оптимистично настроенный и с отличным чувством юмора"
    
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
            TelegramPoster(chat_id='@cto_in_fire', processor=tagadder),
            VkPoster(group_id='229837981', processor=tagadder)
        ]

    def __init__(self, posters=None, force_rebuild=False):
        super().__init__(posters=posters or self._posters(), force_rebuild=force_rebuild)

class LegendaryCtoReviewer(LegendaryCtoBlogger):
    def _check_task(self, task, days_before=1, **_):
        return super()._check_task(task, days_before, **_)
    
def review():
    blogger = LegendaryCtoReviewer(
        posters=[TelegramPoster(processor=tagadder)]
    )
    blogger.post()

def post():
    blogger = LegendaryCtoBlogger()
    blogger.post()

def init():
    editor = Editor(root_folder)
    editor.init_project()

def make_tasks():
    editor = Editor(root_folder)
    editor.create_simple(first_post_date=date(2025, 3, 9), days_between_posts=7)