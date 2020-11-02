from django.conf import settings
from django.core.management.base import BaseCommand
import json
from school.models import Student, Teacher
import os

class Command(BaseCommand):
    help = u'Загрузка данных об учениках и учетилях из json-файла'

    def add_arguments(self, parser):
        parser.add_argument('src_path', type=str, help=u'Путь к файлу с исходными данными')

    def handle(self, *args, **options):
        src_path = options['src_path']
        src_full_path = os.path.join(settings.BASE_DIR, src_path)
        if not os.path.exists(src_full_path):
            print('Не найден файл по указанному адресу:', src_full_path)
            return
        with open(src_full_path, encoding='utf8') as src_file:
            data = json.load(src_file)

        for object in data:
            if object['model'] == 'school.student':
                student = Student.objects.create(id=object['pk'], **object['fields'])
                teacher_id =object['fields'].get('teacher', None)
                if teacher_id:
                    student.teachers.add(Teacher.objects.get(id=teacher_id))

            elif object['model'] == 'school.teacher':
                teacher = Teacher.objects.create(id=object['pk'], **object['fields'])

