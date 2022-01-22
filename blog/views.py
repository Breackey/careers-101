from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from .models import Post, Comment, Category
from .forms import EmailPostForm, CommentForm, SearchForm
from taggit.models import Tag
from django.db.models import Count
from django.core.mail import send_mail
from django.contrib.postgres.search import SearchVector, SearchQuery,SearchRank, TrigramSimilarity
import random
 

Post.objects.annotate(search=SearchVector('title', 'content'),).filter(search='django')



""" class PostListView(ListView):
    queryset = Post.objects.filter(status=1).order_by("-created")
    context_object_name = 'post_list'
    paginate_by = 2
    template_name = 'blog/latest_posts.html' """


 
def post_list(request, tag_slug=None):
       
    posts = Post.published.all()
    tag = None
    categories = Category.objects.all()

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.objects.filter(tags__in=[tag])
    paginator = Paginator(posts, 2) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    all_posts = list(Post.objects.all())
    recent_posts = random.sample(all_posts,3)
    
    context = {'page': page,'posts': posts,'tag': tag,'recent_posts':recent_posts, 'post_list': 'active', 'categories': categories}   
    
    #context = {'page': page,'posts': posts,'tag': tag,'product_list' : productlist , 'category_list' : categorylist , 'count':Category.objects.count()}   
    
    return render(request,
                  'blog/blog.html',
                  context)
   
    
def post_detail(request,slug, year, month, day):
    categories = Category.objects.all()
    post = get_object_or_404(Post, slug=slug,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True).order_by("-created")
    new_comment = None
    if request.method == 'POST':
    # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
    # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
        # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
        
    # List of similar posts
    post_tags_ids = Post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                            .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                            .order_by('-same_tags','-publish')[:4]

    return render(request,
                  'blog/post_detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts,
                   'categories': categories})
    

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
        # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'breackeyawino@gmail.com',
                      [cd['to']])
            sent = True
        # ... send email
    else:
        form = EmailPostForm()
    return render(request, 
                  'blog/post_share.html', 
                  {'post': post,
                    'form': form,
                    'sent': sent})

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'content')
            search_query = SearchQuery(query)
            results = Post.published.annotate(similarity=TrigramSimilarity('title', query),
                                                ).filter(similarity__gt=0.1).order_by('-similarity')
    return render(request,'blog/search.html',
                        {'form': form,
                        'query': query,
                        'results': results})


def category_detail(request, slug):

    category = get_object_or_404(Category, slug=slug)
    post = Post.objects.filter(category=category)
    context = {'category': category, 
                'post':post}

    return render(request, 'blog/category_detail.html', context)