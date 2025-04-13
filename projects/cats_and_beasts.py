from simple_blogger.blogger.auto import AutoCommonBlogger
from simple_blogger.poster.telegram import TelegramPoster
from simple_blogger.poster.vk import VkPoster
from simple_blogger.poster.instagram import InstagramPoster
from simple_blogger.preprocessor.text import TagAdder
from datetime import date

tagadder = TagAdder(['#вмиреживотных', '#животныймир'])

class AnimalBlogger(AutoCommonBlogger):
    def root_folder(self):
        return f"./files/cats_and_beasts"
    
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

    def __init__(self, posters=None, first_post_date=date(2025, 3, 11)):
        super().__init__(posters=posters or self._posters(), first_post_date=first_post_date)

# class AnimalReviewer(AnimalBlogger):
#     def _check_task(self, task, tasks, days_before=1):
#         return super()._check_task(task, tasks, days_before)
    

# def review():
#     blogger = AnimalReviewer(
#         posters=[TelegramPoster(processor=tagadder)],
#         force_rebuild=True
#     )
#     blogger.post()

def post():
    blogger = AnimalBlogger(
        posters=[TelegramPoster(processor=tagadder)],
    )
    blogger.post()

def init():
    blogger = AnimalBlogger()
    blogger.init_project()

def make_tasks():
    blogger = AnimalBlogger()
    blogger.create_auto_tasks(day_offset=-261)
