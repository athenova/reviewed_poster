from simple_blogger.blogger.auto import AutoBlogger
from simple_blogger.poster.telegram import TelegramPoster
from simple_blogger.poster.vk import VkPoster
from simple_blogger.editor import Editor
from simple_blogger.preprocessor.text import TagAdder
from simple_blogger.generator.openai import OpenAiTextGenerator, OpenAiImageGenerator
from datetime import date

tagadder = TagAdder(['#pm', '#projectmanagement', '#it', '#ит', '#айти', '#проблемы', '#решения'])
first_post_date=date(2025, 3, 4)
root_folder = f"./files/verge_of_breakdown"

class PmBlogger(AutoBlogger):
    def root_folder(self):
        return root_folder
    
    def _path_constructor(self, task):
        return f"{task['category']}/{task['topic']}"
    
    def _system_prompt(self):
        return f"Ты - проектный менеджер, лидер проекта со 100% харизмой, всегда оптимистично настроенный и с отличным чувством юмора"
    
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
            TelegramPoster(chat_id='@verge_of_breakdown', processor=tagadder),
            VkPoster(group_id='229837997', processor=tagadder)
        ]

    def __init__(self, posters=None, first_post_date=first_post_date, force_rebuild=False):
        super().__init__(posters=posters or self._posters(), first_post_date=first_post_date, force_rebuild=force_rebuild)

class PmReviewer(PmBlogger):
    def _check_task(self, task, tasks, days_before=1):
        return super()._check_task(task, tasks, days_before)
    
def review():
    blogger = PmReviewer(
        posters=[TelegramPoster(processor=tagadder)],
        force_rebuild=True
    )
    blogger.post()

def post():
    blogger = PmBlogger()
    blogger.post()

def init():
    editor = Editor(root_folder)
    editor.init_project()

def make_tasks():
    editor = Editor(root_folder)
    editor.create_auto()
