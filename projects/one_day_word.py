from simple_blogger.blogger.basic import SimpleBlogger
from simple_blogger.poster.telegram import TelegramPoster
from simple_blogger.editor import Editor
from simple_blogger.preprocessor.text import TagAdder
from simple_blogger.generator.openai import OpenAiTextGenerator
from datetime import date

tagadder = TagAdder(['#новыеслова', '#развитие'])
root_folder = f"./files/one_day_word"

class SkillBlogger(SimpleBlogger):
    def root_folder(self):
        return root_folder
    
    def _path_constructor(self, task):
        return f"{task['category']}/{task['topic']}"
    
    def _message_prompt_constructor(self, task):
        return f"Дай определение слова '{task['topic']}' тематики '{task['category']}', приведи пример использования, используй не более 150 слов, используй смайлики"
    
    def _image_prompt_constructor(self, task):
        return f"Нарисуй рисунок, вдохновлённый '{task['topic']}' тематики '{task['category']}'"
        
    def _message_generator(self):
        return OpenAiTextGenerator(self._system_prompt())
    
    def _posters(self):
        return [
            TelegramPoster(chat_id='@one_day_word', processor=tagadder)
        ]

    def __init__(self, posters=None):
        super().__init__(posters=posters or self._posters())

class SkillReviewer(SkillBlogger):
    def _check_task(self, task, days_before=1, **_):
        return super()._check_task(task, days_before, **_)

def review():
    blogger = SkillReviewer(
        posters=[TelegramPoster(processor=tagadder)]
    )
    blogger.post()

def post():
    blogger = SkillBlogger()
    blogger.post()

def init():
    editor = Editor(root_folder)
    editor.init_project()

def make_tasks():
    editor = Editor(root_folder)
    first_post_date=date(2025, 3, 13)
    editor.create_simple(first_post_date=first_post_date)
