from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.contrib.auth import logout, login
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Article, Category, User, Comment
from .forms import ArticleForm, LoginForm, RegistrationForm, CommentForm
from django.db.models import Q

# Create your views here.


class ArticleList(LoginRequiredMixin, ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'blog/all_articles.html'
    extra_context = {
        "title": "Maqolalar ro'yxati"
    }
    paginate_by = 6

    def get_queryset(self):
        return Article.objects.filter(is_published=True).select_related('category')


class ArticleDetail(LoginRequiredMixin, DetailView):
    model = Article

    def get_queryset(self):
        return Article.objects.filter(pk=self.kwargs['pk'], is_published=True).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article = Article.objects.get(pk=self.kwargs['pk'])
        article.view += 1
        article.save()
        context['title'] = article.title


        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()

        context['comments'] = Comment.objects.all()

        articles = Article.objects.order_by('-view')[:4]
        context['articles'] = articles


        return context


class NewArticle(LoginRequiredMixin, CreateView):
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    extra_context = {
        'title': "Class yordamida maqola qo'shish"
    }
    success_url = reverse_lazy('index')


class ArticleListByCategory(ArticleList):

    def get_queryset(self):
        return Article.objects.filter(category_id=self.kwargs['pk'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = category.title
        return context


class SearchResults(ArticleList):

    def get_queryset(self):
        word = self.request.GET.get('q')
        articles = Article.objects.filter(
            Q(title__icontains=word) |
            Q(content__icontains=word),
            is_published=True
        )
        return articles


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'


class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('index')
    context_object_name = 'article'


@login_required
def profile(request, user_id):
    if request.user.is_authenticated:
        # pk = request.user.pk
        user = User.objects.get(pk=user_id)

        articles = Article.objects.filter(author=user)

        context = {
            'title': "Sizning profilingiz!",
            'user': user,
            'articles': articles
        }
        messages.success(request, "Xush kelibsiz zoti oliylari😍")
        return render(request, "blog/profile.html", context)
    else:
        messages.warning(request, "Avval saytga kir bratishka😁")
        return redirect('login')



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Siz Avtorizatsiyadan muvaffaqiyatli o'tdingiz!")
            return redirect('index')
    else:
        form = LoginForm()

    context = {
        'form': form,
        'title': 'Avtorizatsiya'
    }
    return render(request, 'blog/user_login.html', context)


def user_logout(request):
    logout(request)
    messages.warning(request, "Siz saytdan chiqdingiz!")
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Akkount muvaffaqiyatli ochildi!")
            return redirect('login')
        else:
            messages.error(request, "Registratsiyada hatolik!")
    else:
        form = RegistrationForm()

    context = {
        'title': "Account ochish",
        'form': form
    }
    return render(request, 'blog/register.html', context)


def add_comment(request, article_id):
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        article = Article.objects.get(pk=article_id)
        comment.article = article
        comment.save()
        messages.success(request, "Sizning iliq fikrlaringiz qo'shildi!!!")
    else:
        pass
    return redirect('article_details', article_id)









# def test(request):
#     articles = Article.objects.all()
#     paginator = Paginator(articles, 2)
#     page_number = request.GET.get('page')
#     page_articles = paginator.get_page(page_number)
#
#     context = {
#         'page_articles': page_articles
#     }
#     return render(request, 'blog/all_articles.html', context)






# def index(request):
#     # categories = Category.objects.all()
#     articles = Article.objects.filter(is_published=True)
#     context = {
#         "title": "Maqolalar ro'yxati",
#         "articles": articles,
#         # "categories": categories
#     }
#     return render(request, 'blog/all_articles.html', context=context)


# def category_list(request, pk):
#     # categories = Category.objects.all()
#     articles = Article.objects.filter(category_id=pk, is_published=True)
#     context = {
#         "title": 'Kategoriya',
#         "articles": articles,
#         # "categories": categories
#     }
#     return render(request, 'blog/all_articles.html', context=context)


# def article_details(request, pk):
#     article = get_object_or_404(Article, pk=pk, is_published=True)
#     context = {
#         'title': article.title,
#         'article': article
#     }
#     return render(request, 'blog/details.html', context)


# def add_article(request):
#     if request.method == 'POST':
#         form = ArticleForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             article = Article.objects.create(**form.cleaned_data)
#             article.save()
#             return redirect('article_details', article.pk)
#     else:
#         form = ArticleForm()
#     context = {
#         'form': form,
#         'title': "Maqola qo'shish"
#     }
#     return render(request, 'blog/article_form.html', context)