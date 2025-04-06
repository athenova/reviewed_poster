from simple_blogger.blogger.auto import AutoBlogger
from simple_blogger.poster.TelegramPoster import TelegramPoster
from simple_blogger.poster.VkPoster import VkPoster
from simple_blogger.poster.InstagramPoster import InstagramPoster
from simple_blogger.editor import Editor
from simple_blogger.preprocessor.text import TagAdder
from datetime import date

tagadder = TagAdder(['#вмиреживотных', '#животныймир'])
first_post_date=date(2025, 3, 11)
root_folder = f"./files/cats_and_beasts"

class AnimalBlogger(AutoBlogger):
    def root_folder(self):
        return root_folder
    
    def _system_prompt(self):
        return "Ты - специалист по животным, блоггер с 1000000 подписчиков, умеющий заинтересовать аудиторию в изучении животного мира"
    
    def _path_constructor(self, task):
        return f"{task['family']},{task['genus']}/{task['species']}"
    
    def _message_prompt_constructor(self, task):
        return f"Расскажи интересный факт о животном породы '{task['species']}' из рода '{task['genus']}' семейства '{task['family']}', используй не более 100 слов"
    
    def _image_prompt_constructor(self, task):
        return f"Нарисуй животное породы '{task['species']}' из рода '{task['genus']}' семейства '{task['family']}'. Эстетично, красиво, реалистично, крупным планом"
        
    def _posters(self):
        return [
            TelegramPoster(chat_id='@cats_and_beasts', processor=tagadder),
            VkPoster(group_id='229821868', processor=tagadder),
            InstagramPoster(account_token_name='CATS_AND_BEASTS_TOKEN', processor=tagadder)
        ]

    def __init__(self, posters=None, first_post_date=first_post_date, force_rebuild=False):
        super().__init__(posters=posters or self._posters(), first_post_date=first_post_date, force_rebuild=force_rebuild)

class AnimalReviewer(AnimalBlogger):
    def _check_task(self, task, tasks, days_before=1):
        return super()._check_task(task, tasks, days_before)
    

def review():
    blogger = AnimalReviewer(
        posters=[TelegramPoster(processor=tagadder)],
        force_rebuild=True
    )
    blogger.post()

def post():
    blogger = AnimalBlogger()
    blogger.post()

def init():
    editor = Editor(root_folder)
    editor.init_project()

def make_tasks():
    editor = Editor(root_folder)
    editor.create_auto(day_offset=-261)