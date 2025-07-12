from encodings.punycode import T
from django.db import models
from django.db.models import CASCADE
from .consts import MAX_RATE
# カテゴリの３つの情報を扱えるようにする。カッコ内右の値がhtmlで表示、左の値がPythonやhtmlコードで使用
CATEGORY = (('business', 'ビジネス'), ('life', '生活'), ('other', 'その他'))

RATE_CHOICES = [(x, str(x)) for x in range(0, MAX_RATE + 1)]

# 書籍のモデル
class Book(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    # nullはデータベースが空で許容、blankはフォームに入力されたデータが空でも許容する
    thumbnail = models.ImageField(null=True, blank=True)
    category = models.CharField(
                max_length=100,
                choices=CATEGORY
                )
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    # オブジェクトの文字列を返す 
    def __str__(self):
        return self.title

# レビューのモデル
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    rate = models.IntegerField(choices=RATE_CHOICES)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title