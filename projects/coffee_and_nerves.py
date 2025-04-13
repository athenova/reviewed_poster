from simple_blogger.blogger.auto.cached import CachedAutoSimpleBlogger
from simple_blogger.poster.telegram import TelegramPoster
from simple_blogger.poster.vk import VkPoster
from simple_blogger.preprocessor.text import TagAdder
from simple_blogger.generator.openai import OpenAiTextGenerator, OpenAiImageGenerator
from datetime import date

tagadder = TagAdder(['#hr', '#кадры', '#it', '#ит', '#айти', '#проблемы', '#решения'])

class HrBlogger(CachedAutoSimpleBlogger):
    def root_folder(self):
        return f"./files/coffee_and_nerves"
    
    def _path_constructor(self, task):
        return f"{task['category']}/{task['topic']}"
    
    def _system_prompt(self):
        return 'Ты - руководитель HR, лидер команды со 100% харизмой, всегда оптимистично настроенный и с отличным чувством юмора'
    
    def _message_prompt_constructor(self, task):
        return f"Выбери рандомно актуальную проблему по теме '{task['topic']}' из области '{task['category']}', опиши проблему, как если бы рассказывал подруге, выбери рандомно метод решения, опиши метод решения, используй смайлики, используй менее 100 слов"
    
    def _image_prompt_constructor(self, task):
        return f"Нарисуй картинку, вдохновлённую темой '{task['topic']}' из области '{task['category']}'"
    
    def _message_generator(self):
        return OpenAiTextGenerator(self._system_prompt())
    
    def _image_generator(self):
        return OpenAiImageGenerator()
        
    def _posters(self):
        return [
            TelegramPoster(chat_id='@coffee_and_nerves', processor=tagadder),
            VkPoster(group_id='229838019', processor=tagadder)
        ]

    def __init__(self, posters=None, first_post_date=date(2025, 3, 6), force_rebuild=False):
        super().__init__(posters or self._posters(), first_post_date, force_rebuild)

class HrReviewer(HrBlogger):
    def _check_task(self, task, tasks, days_before=1):
        return super()._check_task(task, tasks, days_before)
    
def review():
    blogger = HrReviewer(
        posters=[TelegramPoster(processor=tagadder)],
        force_rebuild=True
    )
    blogger.post()

def post():
    blogger = HrBlogger()
    blogger.post()

def init():
    blogger = HrBlogger()
    blogger.init_project()

def make_tasks():
    blogger = HrBlogger()
    blogger.create_auto_tasks()