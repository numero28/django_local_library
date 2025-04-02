
import datetime
from django.shortcuts import render, get_object_or_404
from .models import Book, Author, Genre, BookInstance
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm


# Create your views here.


def index(request):

    # Generate counts of some of the main objects
    num_of_books = Book.objects.all().count
    num_of_instances = BookInstance.objects.all().count
    num_of_genres = Genre.objects.filter(name__exact='Fantasy').count

    # Available books (status = 'a')
    num_of_instances_available = BookInstance.objects.filter(
        status__exact='a').count

    # The 'all()' is implied by default.
    num_of_authors = Author.objects.count

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_of_books': num_of_books,
        'num_of_instances': num_of_instances,
        'num_of_instances_available': num_of_instances_available,
        'num_of_authors': num_of_authors,
        'num_visits': num_visits,
        'num_of_genres' : num_of_genres
    }

    return render(request, 'catalog/index.html', context)


@login_required
def book(request):
    paginate_by = 2
    books = Book.objects.all().values()
    return render(request, 'catalog/book.html', {'books': books})


@login_required
def author(request):
    authors = Author.objects.all().values()
    return render(request, 'catalog/author.html', {'authors': authors})


class BookListView(generic.ListView):
    model = Book

    # your own name for the list as a template variable
    context_object_name = 'book_list'
    queryset = Book.objects.filter(title__icontains='war')[
        :5]  # Get 5 books containing the title war
    # Specify your own template name/location
    template_name = 'templates/book_list.html'


'''
    def get_queryset(self):
        return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context
'''


class AuthorListView(generic.ListView):
    model = Author


def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    return render(request, 'catalog/book_detail.html', {'book': book, })


def author_detail(request, pk):
    author_details = Author.objects.get(pk=pk)
    return render(request, 'catalog/author_detail.html', {'author_details': author_details})


def login(request):
    return render(request, 'registration/login.html')


def logout(request):
    return render(request, 'registration/logout.html')


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )


class LoanedBooksByLibrarianListView(generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_librarian.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )


def form(request):
    return render(request, 'catalog/test_form.html')


def form_detail(request, name):
    idx = name
    return render(request, 'catalog/test_form_detail.html', {'idx': idx})

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)