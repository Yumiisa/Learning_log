from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def home(request):
    """home page for learning log"""
    return render(request, "learning_logs/home.html")


@login_required
def check_topic_owner(topic, request):
    if not topic.public:
        if topic.owner != request.user:
            raise Http404


@login_required
def topics(request):
    """Get public topic"""
    public_topics = Topic.objects.filter(public=True)
    # Get private topic and append public topic
    if request.user.is_authenticated:
        private_topics = Topic.objects.filter(owner=request.user)
        topics = public_topics.union(private_topics).order_by("date_added")
    else:
        topics = public_topics
    context = {"topics": topics}
    return render(request, "learning_logs/topics.html", context)


@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    """Make sure topic belongs to current user"""
    if not topic.public:
        if topic.owner != request.user:
            raise Http404

    entries = topic.entry_set.order_by("-date_added")
    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)


@login_required
def new_topic(request):
    """add a new topic"""
    if request.method != "POST":
        # No data submitted create blANK form
        form = TopicForm()
    else:
        # post data submitted; process data
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse("topics"))
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


@login_required
def new_entry(request, topic_id):
    """add new entry for particular topic"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != "POST":
        """No data submitted; create a blank form"""
        form = EntryForm()
    else:
        # post data submitted; process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse("topic", args=[topic_id]))
    context = {"topic": topic, "form": form}
    return render(request, "learning_logs/new_entry.html", context)


@login_required
def edit_entry(request, entry_id):
    """ "edit existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    """make sure entry belongs to current user"""
    if topic.owner != request.user:
        raise Http404
    if request.method != "POST":
        """Initial request ; prefill form with current entry"""
        form = EntryForm(instance=entry)
    else:
        # post data submitted, process data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("topic", args=[topic.id]))
    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "learning_logs/edit_entry.html", context)
