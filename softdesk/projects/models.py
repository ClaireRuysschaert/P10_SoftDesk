import uuid

from django.db import models

from softdesk.accounts.models import SoftUser, Contributor


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        SoftUser, on_delete=models.CASCADE, related_name="authored_projects"
    )
    type = models.CharField(
        max_length=3,
        choices=[
            ("BAE", "back-end"),
            ("FRE", "front-end"),
            ("IOS", "iOs"),
            ("AND", "Android"),
        ],
    )
    contributors = models.ManyToManyField(
        SoftUser, through=Contributor, related_name="contributed_projects"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        have_not_been_created = not self.pk
        super().save(*args, **kwargs)
        if have_not_been_created:
            self.contributors.add(self.author)


class Issue(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(
        SoftUser, on_delete=models.CASCADE, related_name="authored_issues"
    )
    assign_to = models.ForeignKey(
        SoftUser, on_delete=models.CASCADE, related_name="assigned_issues"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="issues"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=4,
        choices=[
            ("TODO", "to do"),
            ("WIP", "work in progress"),
            ("END", "finished"),
        ],
        default="TODO",
    )
    priority = models.CharField(
        max_length=3,
        choices=[
            ("LOW", "low"),
            ("MED", "medium"),
            ("HIG", "high"),
        ],
        default="LOW",
    )
    tag = models.CharField(
        max_length=4,
        choices=[
            ("BUG", "bug"),
            ("TASK", "task"),
            ("FEAT", "feature"),
        ],
        default="TASK",
    )

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(
        SoftUser, on_delete=models.CASCADE, related_name="authored_comments"
    )
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.content
