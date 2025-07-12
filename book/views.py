from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, DeleteView, UpdateView,
    )
from .models import Book, Review
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.core.paginator import Paginator
# １ページに表示する書籍データの数を定義
from .consts import ITEM_PER_PAGE

def index_view(request):
    # Bookモデルのオブジェクトをカテゴリ順に取得
    object_list = Book.objects.order_by('-id')
    # 星の数ランキング順に取得 # review__rateはrivewが対象とするモデル、rateがそのモデルのフィールド
    ranking_list = Book.objects.annotate(avg_rating=Avg('review__rate')).order_by('-avg_rating')
    # Paginatorで書籍データ2つで１セットのオブジェクトを作成
    pagenator = Paginator(ranking_list, ITEM_PER_PAGE)
    # request.GETでURLのページ番号を取得  get('page', 1)でpageというクエリがあればその値をなければ1を返す
    page_number = request.GET.get('page', 1)
    # page_numberオブジェクトを格納するため
    page_obj = pagenator.page(page_number)

    # <QuerySet [<Book: ビジネス本>, <Book: 料理本>, <Book: webアプリ作成>]>
    return render(request,
        'book/index.html', 
        {'object_list': object_list, 'ranking_list': ranking_list, 'page_obj': page_obj}, 
    )

# LoginRequiredMixin　ログインしている状態のみ表示
class ListBookView(LoginRequiredMixin, ListView):
    # renderの役割
    template_name = 'book/book_list.html'
    model = Book
    # ページ
    paginate_by = ITEM_PER_PAGE

class DetailBookView(LoginRequiredMixin, DetailView):
    template_name = 'book/book_detail.html'
    model = Book

class CreateBookView(LoginRequiredMixin, CreateView):
    template_name = 'book/book_create.html'
    model = Book
    # モデルのどの項目をフォームに表示するか指定
    fields = ('title', 'text', 'category', 'thumbnail')
    # 画面遷移処理、リクエストがあるまで待機→逆引き
    success_url = reverse_lazy('list-book')
    # ユーザー情報を登録するため
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DeleteBookView(LoginRequiredMixin, DeleteView):
    template_name = 'book/book_confirm_delete.html'
    model = Book
    success_url = reverse_lazy('list-book')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        if obj.user != self.request.user:
            raise PermissionDenied
        
        return obj
        
class UpdateBookView(LoginRequiredMixin, UpdateView):
    template_name = 'book/book_update.html'
    model = Book
    fields = ('title', 'text', 'category', 'thumbnail')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # 書籍登録したユーザーとログイン中のユーザーが等しくない時
        if obj.user != self.request.user:
            # 強制的に例外の表示
            raise PermissionDenied    
        
        return obj
    
    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk': self.object.id})

class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ('book', 'title', 'text', 'rate')
    template_name = 'book/review_form.html'
    # 対象書籍のデータを取得 <int:book_id>が数値として**kwargsに渡される
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Book.objects.get(pk=self.kwargs['book_id'])
        return context
    # ログインユーザー情報を取得
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    # 遷移画面を設定 self.object は 投稿が成功して保存された Review インスタンス self.object.book.id は そのレビューが属する書籍のID
    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk': self.object.book.id})