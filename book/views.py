from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)
from .models import Book, Review, LikeForBook
from django.db.models import Avg

from django.core.paginator import Paginator
from .consts import ITEM_PER_PAGE

from .forms import SearchForm #-----検索機能

import time

import sys
sys.path.append('../')
from accounts.models import Profile

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

class ListBookView(LoginRequiredMixin, ListView):
    template_name = 'book/book_list.html'
    model = Book
    paginate_by = ITEM_PER_PAGE

class DetailBookView(LoginRequiredMixin, DetailView):
    template_name = 'book/book_detail.html'
    model = Book
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        like_for_book_count = self.object.likeforbook_set.count()
        # ポストに対するイイね数
        context['like_for_book_count'] = like_for_book_count
        # ログイン中のユーザーがイイねしているかどうか
        if self.object.likeforbook_set.filter(user=self.request.user).exists():
            context['is_user_liked_for_book'] = True
        else:
            context['is_user_liked_for_book'] = False
        return context

def like_for_book(request):
    book_pk = request.POST.get('book_pk')
    context = {
        'user': f'{request.user.last_name} {request.user.first_name}',
    }
    book = get_object_or_404(Book, pk=book_pk)
    like = LikeForBook.objects.filter(target=book, user=request.user)

    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        like.create(target=book, user=request.user)
        context['method'] = 'create'

    context['like_for_book_count'] = book.likeforbook_set.count()

    return JsonResponse(context)

class CreateBookView(LoginRequiredMixin, CreateView):
    template_name = 'book/book_create.html'
    model = Book
    fields = ('title', 'text', 'category', 'thumbnail')
    success_url = reverse_lazy('list-book')

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
    success_url = reverse_lazy('list-book')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user:
            raise PermissionDenied

        return obj

def index_view(request):
    #-----↓検索機能で追加したやつ↓-----
    searchForm = SearchForm(request.GET)
    if searchForm.is_valid(): # 正常な値が入力されていれば
        keyword = searchForm.cleaned_data['keyword'] #入力された値をKeywordに代入
        books = Book.objects.filter(title__contains=keyword)
    else:
        searchForm = SearchForm()
        books = Book.objects.all()
    books = books.order_by('-id')
    #-----↑検索機能で追加したやつ↑-----
    ranking_list = Book.objects.annotate(avg_rating=Avg('review__rate')).order_by('-avg_rating')
    paginator = Paginator(ranking_list, ITEM_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)
    context = {
        'ranking_list': ranking_list,
        'page_obj': page_obj,
        #booksとsearchFormは検索機能用
        'books': books,
        'searchForm': searchForm,
    }
    return render(
        request,
        'book/index.html',
        context
        ) 

class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ('book', 'title', 'text', 'rate')
    template_name = 'book/review_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Book.objects.get(pk=self.kwargs['book_id'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk': self.object.book.id})


def savebook_list_view(request):
    object_list = Book.objects.all()
    profile1 = Profile.objects.get(pk=request.user.id) # profile1に一人分のプロフィールデータが入る
    save_book_id = profile1.save_book_id # profile1の本の並び順をidで取得する
    print(f'保存された書籍データのid:{save_book_id}')
    # ----------↓設定されている順番に並び替える↓----------
    books_dict = dict([(book.id, book) for book in object_list]) # [id: そのidのBookデータ]という形で辞書に収める
    sorted_books = [books_dict[int(id)] for id in save_book_id] # 表示したい並び順でidの入っているリストで繰り返し処理して、その本情報をsorted_booksに積めていく
    print(f"並び替えられた書籍データ:{sorted_books}")
    # ----------↑設定されている順番に並び替える↑----------
    return render(
    request,
    'book/book_save_list.html',
    {"object_list": object_list, "sorted_books": sorted_books}
    )

def savebook_orderchange_view(request):
    # ----------↓object_listに全書籍データを代入↓----------
    object_list = Book.objects.all()
    # ----------↓profile1にログインしているユーザーのプロフィール情報を代入↓----------
    profile1 = Profile.objects.get(pk=request.user.id) # profile1に一人分のプロフィールデータが入る
    # ----------↓profile1の本の並び順を取得する↓----------
    order_list = profile1.save_book_id
    object_pk_list = []
    for obj in object_list:
        object_pk_list.append(obj.pk)
    # print(f"全書籍のid(object_pk_list):{object_pk_list}")
    # print(f"ユーザーの並び変え順(order_list):{order_list}")
    # ----------↓設定されている順番に並び替える↓----------
    books_dict = dict([(book.id, book) for book in object_list]) # [id: そのidのBookデータ]という形で辞書に収める
    sorted_books_list = [books_dict[int(id)] for id in order_list] # 表示したい並び順でidの入っているリストで繰り返し処理して、その本情報をsorted_booksに積めていく
    # print(f"idとデータの辞書(book_dict):{books_dict}")
    print(f"並び替えられた書籍データ（sorted_books_list）:{sorted_books_list}")
    # ----------↑設定されている順番に並び替える↑----------
    # ----------↓並び替え確定のボタンが押されてリクエストが来た時の分岐↓----------
    if (request.method == 'POST'):
        new_order = request.POST['submit'].split(",") # new_orderに並び替えた後のデータをリスト型で保管する
        # print(f"html側から受け取ったもの：{new_order}") # htmlから渡されたものを確認する
        profile1.save_book_id = new_order # プロフィールのsave_book_idに上書き
        profile1.save() # 変更を保存
        print(f"並び替え後のlist：{profile1.save_book_id}") # profileテーブルの内容が上書きされているかを確認する
        return redirect('list-savebook')
    # ----------↑並び替え確定のボタンが押されてリクエストが来た時の分岐↑----------
    # ----------↓並び替えするためにリクエストが来た時の分岐↓----------
    else:
        context = {
            "object_list": object_list, # 全書籍データ
            "object_pk_list": object_pk_list, # 全書籍データ（idのみ）
            "order_list": order_list, # ユーザーの並び替え順（idのみ）
            "books_dict": books_dict, # {id: その書籍データ}と、辞書型で全書籍データがある
            "sorted_books_list": sorted_books_list, # 並び替え順で書籍データが詰まっている（リスト型）
        }
        return render(
        request,
        'book/order_change.html',
        context)
    # ----------↑並び替えするためにリクエストが来た時の分岐↑----------

def savebook_append(request):
    object_list = Book.objects.all()
    profile1 = Profile.objects.get(pk=request.user.id)
    # ----------追加ボタンが押された分岐----------
    if request.method == 'POST':
        append_book = request.POST.getlist('office')
        for book_id in append_book:
            profile1.save_book_id.append(book_id)
        profile1.save()
        return redirect('list-savebook')
    # ----------
    else:
        # ----------↓obj_li_pkに全書籍のidを詰め込む↓----------
        obj_li_pk = []
        for obj in object_list:
            obj_li_pk.append(obj.id)
        # ----------
        # ----------↓obj_li_pkの中から、既に保存している書籍は削除する↓----------
        for item in profile1.save_book_id:
            obj_li_pk.remove(int(item))
        print(f'{profile1.user}の保存していない書籍番号:{obj_li_pk}')
        books_dict = dict([(book.id, book) for book in object_list]) # [id: そのidのBookデータ]という形で辞書に収める
        nosave_books_list = [books_dict[int(id)] for id in obj_li_pk] # 表示したい並び順でidの入っているリストで繰り返し処理して、その本情報をsorted_booksに積めていく
        # ----------↑obj_li_pkの中から、既に保存している書籍は削除する↑----------
        return render(
            request,
            'book/savebook_append.html',
            {'nosave_books_list': nosave_books_list} # 表示する書籍データがリスト形で詰まっている
    )

def bookorder_delete(request):
    profile1 = Profile.objects.get(pk = request.user.id)
    # ----------削除ボタンが押された分岐----------
    if request.method == 'POST':
        delete_book = request.POST.getlist('office')
        for book_id in delete_book:
            profile1.save_book_id.remove(book_id)
        profile1.save()
        return redirect('list-savebook')
    # ----------
    # ----------削除画面にアクセスする----------
    else:
        object_list = Book.objects.all()
        save_book_id = profile1.save_book_id # profile1の本の並び順をidで取得する
        print(f'保存された書籍データのid:{save_book_id}')
        # ----------↓設定されている順番に並び替える↓----------
        books_dict = dict([(book.id, book) for book in object_list]) # [id: そのidのBookデータ]という形で辞書に収める
        sorted_books = [books_dict[int(id)] for id in save_book_id] # 表示したい並び順でidの入っているリストで繰り返し処理して、その本情報をsorted_booksに積めていく
        print(f"並び替えられた書籍データ:{sorted_books}")
        # ----------↑設定されている順番に並び替える↑----------
        return render(request, 'book/savebook_delete.html',
        {
            'sorted_books': sorted_books,
        })