from simple_blogger.blogger.finite.cached import CachedFiniteSimpleBlogger
from simple_blogger.poster.telegram import TelegramPoster
from simple_blogger.poster.vk import VkPoster
from simple_blogger.poster.instagram import InstagramPoster
from simple_blogger.preprocessor.text import TagAdder
from simple_blogger.generator.openai import OpenAiTextGenerator, OpenAiImageGenerator
from datetime import date

tagadder = TagAdder(['#скилы', '#развитие'])

class SkillBlogger(CachedFiniteSimpleBlogger):
    def root_folder(self):
        return f"./files/one_day_skill"
    
    def _path_constructor(self, task):
        return f"{task['group']}/{task['name']}"
    
    def _message_prompt_constructor(self, task):
        return f"Расскажи как {task['name']}, используй не более 100 слов, используй смайлики"
    
    def _image_prompt_constructor(self, task):
        return f"Нарисуй рисунок, вдохновлённый темой '{task['name']}'"
        
    def _message_generator(self):
        return OpenAiTextGenerator(self._system_prompt())
    
    def _image_generator(self):
        return OpenAiImageGenerator()
    
    def _posters(self):
        return [
            TelegramPoster(chat_id='@one_day_skill', processor=tagadder),
            VkPoster(group_id='229822298', processor=tagadder),
            InstagramPoster(account_token_name='ONE_DAY_SKILL_TOKEN', account_id=None, processor=tagadder)
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
    blogger = SkillBlogger()
    blogger.init_project()

def make_tasks():
    blogger = SkillBlogger()
    blogger.create_simple_tasks(first_post_date=date(2025, 3, 16))