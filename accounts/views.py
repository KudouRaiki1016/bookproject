from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import SignupForm

from .models import Profile, Class

from time import sleep

import sys
sys.path.append('../')
from book.models import Book

class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('index')

def signup_view(request):
    # ----------↓POSTメソッドが返された場合（＝サインアップのアカウント作成ボタンが押された場合）↓----------
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # -----↓正常な値が代入されていた時の分岐↓-----
        if form.is_valid():
            form.save() #データベース登録
            # user.refresh_from_db()
            # --↓formに入力された情報を受け取り↓--
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # --↓それをDjangoのデータベースに反映--
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
        # -----
    # ----------
    # ----------↓その他の場合（つまりGETメソッドが返された場合）↓----------
    else:
        form = UserCreationForm()
    # ----------↑その他の場合（つまりGETメソッドが返された場合）↑----------
    return render(request, 'accounts/signup.html', {'form': form})
    # ----------

# from django.db import transaction
# @transaction.atomic
# def create_user(request):
#     if request.method == 'POST':
#         user_form = UserCreationForm(request.POST)
#         if user_form.is_valid():
#             user = user_form.save()
#             user.refresh_from_db() 
#     else:
#         user_form = UserCreationForm()

#     return render(request, 'user_form.html', {
#         'user_form': user_form,
#     })


# def orderlist_view(request, pk):
#     object_list = Book.objects.all()
#     profile = Profile.objects.all() # prifileに全プロフィールデータが入る（できれば一人分のデータのみを取るようにしてスッキリさせたい？）
#     profile1 = Profile.objects.get(pk=pk) # profile1に一人分のプロフィールデータが入る
#     order_list = profile1.book_order # profile1の本の並び順を取得する
#     object_pk_list = []
#     for obj in object_list:
#         object_pk_list.append(obj.pk)
#     print(object_pk_list)
#     print(order_list)
#     # ----------↓並び替え確定のボタンが押されてリクエストが来た時の分岐↓----------
#     if (request.method == 'POST'):
#         sleep(5)
#         new_order = request.POST['submit'].split(",") # new_orderに並び替えた後のデータをリスト型で保管する
#         print(f"html側から受け取ったもの：{new_order}") # htmlから渡されたものを確認する
#         profile1.book_order = new_order # プロフィールのbook_orderに上書き
#         profile1.save() # 変更を保存
#         print(f"afterのlist：{profile1.book_order}") # profileテーブルの内容が上書きされているかを確認する
#         # -----↓変更したものはもう一度定義し直さないとhtml側には古い（変更前の）情報が渡ってしまう（いらないものもありそう？）↓-----
#         object_list = Book.objects.order_by()
#         profile = Profile.objects.all()
#         profile1 = Profile.objects.get(pk=pk)
#         order_list = profile[0].book_order
#         # -----↑変更したものはもう一度定義し直さないとhtml側には古い（変更前の）情報が渡ってしまう（いらないものもありそう？）↑-----
#     # ----------↑並び替え確定のボタンが押されてリクエストが来た時の分岐↑----------
#     context = {
#         "object_list": object_list,
#         "object_pk_list": object_pk_list,
#         "order_list": order_list,
#     }
#     return render(
#     request,
#     'accounts/orderlist.html',
#     context) 

def orderlist_view(request):
    object_list = Book.objects.all()
    profile1 = Profile.objects.get(pk=request.user.id) # profile1に一人分のプロフィールデータが入る
    order_list = profile1.save_book_id # profile1の本の並び順を取得する
    object_pk_list = []
    for obj in object_list:
        object_pk_list.append(obj.pk)
    print(f"全書籍のid:{object_pk_list}")
    print(f"ユーザーの並び変え順:{order_list}")
    # ----------↓設定されている順番に並び替える↓----------
    books_dict = dict([(book.id, book) for book in object_list]) # [id: そのidのBookデータ]という形で辞書に収める
    sorted_books = [books_dict[int(id)] for id in order_list] # 表示したい並び順でidの入っているリストで繰り返し処理して、その本情報をsorted_booksに積めていく
    print(f"並び替えられた書籍データ:{sorted_books}")
    # ----------↑設定されている順番に並び替える↑----------
    context = {
        "object_list": object_list,
        "object_pk_list": object_pk_list,
        "order_list": order_list,
        "sorted_books": sorted_books
    }
    return render(
    request,
    'accounts/orderlist.html',
    context) 

def orderchange_view(request):
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
        return redirect('accounts:orderlist-book')
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
        'accounts/order_change.html',
        context)
    # ----------↑並び替えするためにリクエストが来た時の分岐↑----------

def bookorder_append(request):
    object_list = Book.objects.all()
    profile1 = Profile.objects.get(pk=request.user.id)
    # ----------↓obj_li_pkに全書籍のidを詰め込む↓----------
    obj_li_pk = []
    for obj in object_list:
        obj_li_pk.append(obj.id)
    # ----------↑obj_li_pkに全書籍のidを詰め込む↑----------
    # ----------↓obj_li_pkの中から、既に保存している書籍は削除する↓----------
    for item in profile1.save_book_id:
        obj_li_pk.remove(int(item))
    print(f'{profile1.user}の保存していない書籍番号:{obj_li_pk}')
    books_dict = dict([(book.id, book) for book in object_list]) # [id: そのidのBookデータ]という形で辞書に収める
    display_books_list = [books_dict[int(id)] for id in obj_li_pk] # 表示したい並び順でidの入っているリストで繰り返し処理して、その本情報をsorted_booksに積めていく
    context = {
        'object_list': object_list, # 全書籍データ
        'display_books_list': display_books_list, # 表示する書籍データがリスト形で詰まっている
    }
    return render(
        request,
        'accounts/bookorder_append.html',
        context
)

def bookorder_delete(request, book_id):
    profile1 = Profile.objects.get(pk = request.user.id)
    # ----------削除ボタンが押された分岐----------
    if request.method == 'POST':
        delete_book = request.POST['office']
        print(delete_book)
        # profile1.save_book_id.remove(str(book_id))
        # profile1.save()
        return redirect('accounts:orderlist-book')
    # ----------
    # ----------削除画面にアクセスする----------
    else:
        delete_book = Book.objects.get(pk = book_id)
        return render(request, 'accounts/bookorder_delete.html',
        {
            'delete_book': delete_book,
        })
# from .models import Question # 並び替える対象は『Question』
 
# question_ids = ['q40', 'q30', 'q20', 'q10'] # この順番に並び替えたい
 
# question_qs = Question.objects.filter(question_id__inquestion_ids) # Questionモデルから『question_ids』のみのIDを取得
# ↓ここから並べる↓
# questions_dict = dict([(question.question_id, question) for question in question_qs])　# [id: そのidのQuestionデータ]という形で辞書に収める
# sorted_questions = [questions_dict[id] for id in session_question_ids_list]

# import sys
# sys.path.append('../')
# from book.models import Book
# book_ids = [11, 12]
 
# book_qs = Book.objects.filter(Book.id in book_ids)
 
# books_dict = dict([(book.book_id, book) for book in book_qs])
# sorted_books = [books_dict[id] for id in books_dict]
# print(sorted_books)



# def orderlist_view(request, pk):
#     object_list = Book.objects.all()
#     profile = Profile.objects.all() #prifileに全プロフィールデータが入る（できれば一人分のデータのみを取るようにしてスッキリさせたい？）
#     profile1 = Profile.objects.get(pk=pk) #profile1に一人分のプロフィールデータが入る
#     order_list = profile1.book_order #profile1の本の並び順を取得する
#     #----------↓並び替え確定のボタンが押されてリクエストが来た時の分岐↓----------
#     if (request.method == 'POST'):
#         new_order = request.POST['submit'].split(",") #new_orderに並び替えた後のデータをリスト型で保管する
#         # print(f"html側から受け取ったもの：{new_order}") #htmlから渡されたものを確認する
#         profile1.book_order = new_order # プロフィールのbook_orderに上書き
#         profile1.save() # 変更を保存
#         print(f"afterのlist：{profile1.book_order}") # profileテーブルの内容が上書きされているかを確認する
#         # -----↓変更したものはもう一度定義し直さないとhtml側には古い（変更前の）情報が渡ってしまう（いらないものもありそう？）↓-----
#         object_list = Book.objects.order_by()
#         profile = Profile.objects.all()
#         profile1 = Profile.objects.get(pk=pk)
#         order_list = profile[0].book_order
#         # -----↑変更したものはもう一度定義し直さないとhtml側には古い（変更前の）情報が渡ってしまう（いらないものもありそう？）↑-----
#     # ----------↑並び替え確定のボタンが押されてリクエストが来た時の分岐↑----------
#     context = {
#         "object_list": object_list,
#         "order_list": order_list,
#     }
#     return render(
#     request,
#     'accounts/orderlist.html',
#     context) 

# クラス一覧表示
def class_view(request):
    object_list = Class.objects.all()
    context = {
        'object_list': object_list,
    }
    return render(request, 'accounts/class_list.html', context)

def class_detail_view(request, class_id):
    object = Class.objects.get(pk=class_id)
    context = {
        'object': object,
    }
    return render(request, 'accounts/class_detail.html', context)

def class_member_add_view(request, class_pk):
    object = Class.objects.get(pk=class_pk)
    if request.method == 'POST':
        add_pk_list = request.POST.getlist('members') #リスト型で伝わってくる（中身は文字型）
        for pk in add_pk_list:
            object.members.add(User.objects.get(pk=int(pk)))
        return redirect('accounts:class-detail', class_pk)
    else:
        object_list = User.objects.all()
        # ----------未参加者のリストを作成する----------
        # -----↓全ユーザーのpkリスト作成↓
        all_user_pk_list = []
        for user in object_list:
            all_user_pk_list.append(user.pk)
        # -----
        # -----↓参加済みユーザーのpkリスト作成↓
        attended_user_pk_list = []
        for member in object.members.all():
            attended_user_pk_list.append(member.pk)
        # -----
        # 「未参加ユーザー」 = 「全ユーザー」 - 「参加済みユーザー」
        no_attended_user_pk_list = list(set(all_user_pk_list) - set(attended_user_pk_list))
        no_attended_user_dic = dict((user_pk, User.objects.get(pk=user_pk)) for user_pk in no_attended_user_pk_list)
        no_attended_user_list = [no_attended_user_dic[user_pk] for user_pk in no_attended_user_pk_list]
        # print(all_user_pk_list)
        # print(attended_user_pk_list)
        # print(no_attended_user_pk_list)
        # print(no_attended_user_dic)
        context = {
            'class': object,
            'user_list': no_attended_user_list,
        }
        return render(request, 'accounts/class_members_add.html', context)

def class_member_delete_view(request, class_pk):
    object = Class.objects.get(pk=class_pk)
    if request.method == 'POST':
        delete_pk_list = request.POST.getlist('members') #リスト型で伝わってくる（中身は文字型）
        for pk in delete_pk_list:
            object.members.remove(User.objects.get(pk=int(pk)))
        return redirect('accounts:class-detail', class_pk)
    else:    
        members_list = object.members.all()
        context = {
            'class': object,
            'members_list': members_list,
        }
        return render(request, 'accounts/class_members.delete.html', context)