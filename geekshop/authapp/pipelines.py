from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode
from django.conf import settings
from django.utils import timezone
from social_core.exceptions import AuthException, AuthForbidden
from authapp.models import UserProfile
import requests
import os


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse((
        'http', 'api.vk.com', 'method/users.get', None,
        urlencode(OrderedDict(
            fields=','.join(('bdate', 'sex', 'about', 'photo_max', 'personal')),
            access_token=response['access_token'],
            v=5.131)),
        None)
        )

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]

    if data['sex'] == 1:
        user.userprofile.gender = UserProfile.FEMALE
    elif data['sex'] == 2:
        user.userprofile.gender = UserProfile.MALE
    else:
        pass

    # если есть язык, ставим его
    # если его нет, по умолчанию ставится английский
    try:
        if data['personal']['langs']:
            main_language = data['personal']['langs'][0]

            for key, lang in enumerate(UserProfile.LANGUAGE_CHOICES):
                print(f'key {key} | value {lang} | value[1] {lang[1]}')
                language_key = lang[0]
                language_value = lang[1]

                if main_language == language_value:
                    user.userprofile.language = language_key
                    break
    except KeyError:
        # если у пользователя нет языков, простой if data['personal']['langs'] не работал
        # возможно очень плохой выход, вот так избегать исключения
        # но у нас же по дефолту значение будт ставиться
        pass

    if data['about']:
        user.userprofile.about = data['about']

    bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
    age = timezone.now().date().year - bdate.year
    user.age = age
    if age < 18:
        # TODO:
        # сделать красивую обработку AuthForbidden
        user.delete()
        raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    # сохраняем изображение
    if data['photo_max']:
        # первая реализация, до урока
        # image_url = data['photo_max']
        # image_name = data['photo_max'].split('/')[-1].split('?')[0]
        # image_path_to_save = os.path.join(settings.MEDIA_ROOT, 'users_image', image_name)
        # urllib.request.urlretrieve(image_url, image_path_to_save)
        # user.image = f'users_image/{image_name}'

        image_url = data['photo_max']
        image_response = requests.get(image_url)
        # TODO:
        # подумать над форматом изображения
        image_path_to_save = f'users_image/{user.pk}.jpg'
        with open(os.path.join(settings.MEDIA_ROOT, image_path_to_save), 'wb') as f:
            f.write(image_response.content)
        user.image = image_path_to_save

    user.save()
