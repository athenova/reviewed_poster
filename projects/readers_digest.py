from simple_blogger.blogger.basic import SimpleBlogger
from simple_blogger.poster.TelegramPoster import TelegramPoster
from simple_blogger.poster.VkPoster import VkPoster
from simple_blogger.editor import Editor
from simple_blogger.preprocessor.text import TagAdder
from simple_blogger.generator.yandex import YandexImageGenerator, YandexTextGenerator
from datetime import date

tagadder = TagAdder(['#книги', '#литература', '#чтениеналето'])
root_folder = f"./files/readers_digest"

class ReaderBlogger(SimpleBlogger):
    def root_folder(self):
        return root_folder
    
    def _path_constructor(self, task):
        return f"{task['author']}/{task['book']}"
    
    def _system_prompt(self):
        return f"Ты - школьный блоггер, книгоман, прочитавший более 1000 книг, используешь в разговоре сленг {self.age}-летних подростков и смайлики"
    
    def _message_prompt_constructor(self, task):
        return f"Расскажи {self.age}-летнему подростку без спойлеров, почему стоит прочитать книгу '{task['book']}' автора {task['author']}, используй не более 150 слов"
    
    def _image_prompt_constructor(self, task):
        return f"Нарисуй картинку, вдохновлённую книгой '{task['book']}' автора {task['author']}, крупный план, глубина, гиперреализм"
    
    def _message_generator(self):
        return YandexTextGenerator(self._system_prompt(), model_version='rc')
    
    def _image_generator(self):
        return YandexImageGenerator()
        
    def _posters(self):
        return [
            TelegramPoster(chat_id='@class5nik', processor=tagadder),
            VkPoster(group_id='229821544', processor=tagadder)
        ]

    def __init__(self, age=12, posters=None, force_rebuild=False):
        self.age=12
        super().__init__(posters=posters or self._posters(), force_rebuild=force_rebuild)

class ReaderReviewer(ReaderBlogger):
    def _check_task(self, task, days_before=1, **_):
        return super()._check_task(task, days_before, **_)
    
def review():
    blogger = ReaderReviewer(
        posters=[TelegramPoster(processor=tagadder)]
    )
    blogger.post()

def post():
    blogger = ReaderBlogger()
    blogger.post()

def init():
    editor = Editor(root_folder)
    editor.init_project()

def make_tasks():
    editor = Editor(root_folder)
    editor.create_simple(first_post_date=date(2025, 6, 9), days_between_posts=2)