from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.response import Response
from django.urls import reverse
from softdesk.projects.models import Comment, Issue, Project
from softdesk.accounts.models import SoftUser


class ProjectViewSetTestCase(TestCase):
    def setUp(self):
        self.anonymous_client = APIClient()
        self.noperm_client = APIClient()
        self.noperm_user: SoftUser = SoftUser.objects.create(
            username="no_perm_user",
            email="noperm@mail.com",
            password="nopermpassword",
            birthdate="2022-02-02",
        )
        self.noperm_client.force_authenticate(user=self.noperm_user)
        self.project_user: SoftUser = SoftUser.objects.create(
            username="projecttestuser",
            email="test@mail.com",
            password="testpassword",
            birthdate="2020-01-01",
        )
        self.project_client = APIClient()
        self.project_client.force_authenticate(user=self.project_user)
        self.project = Project.objects.create(
            name="Test Project",
            description="Test Description",
            author=self.project_user,
            type="Task",
        )
        self.contributor_client = APIClient()
        self.contributor = SoftUser.objects.create(
            username="contributor",
            email="contributor@mail.com",
            password="contributorpassword",
            birthdate="2000-01-01",
        )
        self.project.contributors.add(self.contributor)
        self.contributor_client.force_authenticate(user=self.contributor)

    def test_anonymous_user_cannot_access_project(self):
        response: Response = self.anonymous_client.get(reverse("project-detail", args=[self.project.pk]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_only_contributor_and_project_user_can_access_project(self):
        clients_and_responses: list[tuple[APIClient, int]] = [
            (self.anonymous_client, status.HTTP_401_UNAUTHORIZED),
            (self.noperm_client, status.HTTP_403_FORBIDDEN),
            (self.project_client, status.HTTP_200_OK),
            (self.contributor_client, status.HTTP_200_OK),
        ]
        for client, expected_status in clients_and_responses:
            response: Response = client.get(reverse("project-detail", args=[self.project.pk]))
            self.assertEqual(response.status_code, expected_status)

    def test_project_creation(self):
        project_data = {
            "name": "New Project",
            "author": self.project_user.pk,
            "type": "BAE",
        }
        clients_and_responses: list[tuple[APIClient, int]] = [
            (self.anonymous_client, status.HTTP_401_UNAUTHORIZED),
            (self.noperm_client, status.HTTP_201_CREATED),
            (self.project_client, status.HTTP_201_CREATED),
            (self.contributor_client, status.HTTP_201_CREATED),
        ]
        project_number_to_create = 0
        initial_project_count = Project.objects.count()
        for client, expected_status in clients_and_responses:
            project_data["name"] = f"New Project {project_number_to_create}"
            response: Response = client.post(reverse("project-list"), project_data)
            self.assertEqual(response.status_code, expected_status)
            project_number_to_create += 1
            current_project_count = Project.objects.count()
            if expected_status == status.HTTP_201_CREATED:
                self.assertEqual(current_project_count, initial_project_count + 1)
                initial_project_count += 1
            else:
                self.assertEqual(current_project_count, initial_project_count)

    def test_only_project_user_can_edit_project(self):
        original_project_name = self.project.name
        clients_and_responses: list[tuple[APIClient, int]] = [
            (self.anonymous_client, status.HTTP_401_UNAUTHORIZED),
            (self.noperm_client, status.HTTP_403_FORBIDDEN),
            (self.contributor_client, status.HTTP_403_FORBIDDEN),
            (self.project_client, status.HTTP_200_OK),
        ]
        for client, expected_status in clients_and_responses:
            response: Response = client.patch(reverse("project-detail", args=[self.project.pk]), {"name": "New Name"}
            )
            self.assertEqual(response.status_code, expected_status)
            self.project.refresh_from_db()
            self.assertEqual(
                self.project.name,
                original_project_name if client != self.project_client else "New Name",
            )

    def test_only_project_user_can_delete_project(self):
        clients_and_responses: list[tuple[APIClient, int]] = [
            (self.anonymous_client, status.HTTP_401_UNAUTHORIZED),
            (self.noperm_client, status.HTTP_403_FORBIDDEN),
            (self.contributor_client, status.HTTP_403_FORBIDDEN),
            (self.project_client, status.HTTP_204_NO_CONTENT),
        ]
        for client, expected_status in clients_and_responses:
            response: Response = client.delete(reverse("project-detail", args=[self.project.pk]))
            self.assertEqual(response.status_code, expected_status)


class IssueViewSetTestCase(TestCase):
    def setUp(self):
        self.anonymous_client = APIClient()
        self.noperm_client = APIClient()
        self.noperm_user: SoftUser = SoftUser.objects.create(
            username="no_perm_user",
            email="noperm@mail.com",
            password="nopermpassword",
            birthdate="2022-02-02",
        )
        self.noperm_client.force_authenticate(user=self.noperm_user)
        self.issue_user: SoftUser = SoftUser.objects.create(
            username="issuetestuser",
            email="test@mail.com",
            password="testpassword",
            birthdate="2020-01-01",
        )
        self.issue_client = APIClient()
        self.issue_client.force_authenticate(user=self.issue_user)
        self.project = Project.objects.create(
            name="Test Project",
            description="Test Description",
            author=self.issue_user,
            type="BAE",
        )
        self.issue = Issue.objects.create(
            name="Test Issue",
            description="Test Description",
            tag="BUG",
            priority="HIG",
            project=self.project,
            author=self.issue_user,
            assign_to=self.issue_user,
        )
        self.contributor_client = APIClient()
        self.contributor = SoftUser.objects.create(
            username="contributor",
            email="contributor@mail.com",
            password="contributorpassword",
            birthdate="2000-01-01",
        )
        self.project.contributors.add(self.contributor)
        self.contributor_client.force_authenticate(user=self.contributor)

    def test_anonymous_user_cannot_access_issue(self):
        response: Response = self.anonymous_client.get(reverse("issue-detail", args=[self.issue.pk]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_only_contributor_and_issue_user_can_access_issue(self):
        clients_and_responses: list[tuple[APIClient, int]] = [
            (self.anonymous_client, status.HTTP_401_UNAUTHORIZED),
            (self.noperm_client, status.HTTP_403_FORBIDDEN),
            (self.issue_client, status.HTTP_200_OK),
            (self.contributor_client, status.HTTP_200_OK),
        ]
        for client, expected_status in clients_and_responses:
            response: Response = client.get(reverse("issue-detail", args=[self.issue.pk]))
            self.assertEqual(response.status_code, expected_status)

    def test_issue_creation(self):
        issue_data = {
            "name": "New Issue",
            "description": "New Description",
            "project": self.project.pk,
            "author": self.issue_user.pk,
            "assign_to": self.contributor.pk,
        }
        clients_and_responses: list[tuple[APIClient, int]] = [
            (self.anonymous_client, status.HTTP_401_UNAUTHORIZED),
            (self.noperm_client, status.HTTP_403_FORBIDDEN),
            (self.issue_client, status.HTTP_201_CREATED),
            (self.contributor_client, status.HTTP_201_CREATED),
        ]
        issue_number_to_create = 0
        initial_issue_count = Issue.objects.count()
        for client, expected_status in clients_and_responses:
            issue_data["name"] = f"New Issue {issue_number_to_create}"
            response: Response = client.post(reverse("issue-list"), issue_data)
            self.assertEqual(response.status_code, expected_status)
            issue_number_to_create += 1
            current_issue_count = Issue.objects.count()
            if expected_status == status.HTTP_201_CREATED:
                self.assertEqual(current_issue_count, initial_issue_count + 1)
                initial_issue_count += 1
            else:
                self.assertEqual(current_issue_count, initial_issue_count)

    def test_only_issue_user_can_edit_issue(self):
        original_issue_title = self.issue.name
        clients_and_responses: list[tuple[APIClient, int]] = [
            (self.anonymous_client, status.HTTP_401_UNAUTHORIZED),
            (self.noperm_client, status.HTTP_403_FORBIDDEN),
            (self.contributor_client, status.HTTP_403_FORBIDDEN),
            (self.issue_client, status.HTTP_200_OK),
        ]
        for client, expected_status in clients_and_responses:
            response: Response = client.patch(reverse("issue-detail", args=[self.issue.pk]), {"name": "New Title"})
            self.assertEqual(response.status_code, expected_status)
            self.issue.refresh_from_db()
            self.assertEqual(
                self.issue.name,
                original_issue_title if client != self.issue_client else "New Title",
            )

    def test_only_issue_user_can_delete_issue(self):
        clients_and_responses: list[tuple[APIClient, int]] = [
            (self.anonymous_client, status.HTTP_401_UNAUTHORIZED),
            (self.noperm_client, status.HTTP_403_FORBIDDEN),
            (self.contributor_client, status.HTTP_403_FORBIDDEN),
            (self.issue_client, status.HTTP_204_NO_CONTENT),
        ]
        for client, expected_status in clients_and_responses:
            response: Response = client.delete(reverse("issue-detail", args=[self.issue.pk]))
            self.assertEqual(response.status_code, expected_status)

    def test_assign_to_must_be_contributor_of_project(self):
        issue_data = {
            "name": "New Issue",
            "description": "New Description",
            "project": self.project.pk,
            "author": self.issue_user.pk,
            "assign_to": self.noperm_user.pk,
        }
        clients_and_responses: list[tuple[APIClient, int]] = [
            (self.anonymous_client, status.HTTP_401_UNAUTHORIZED),
            (self.noperm_client, status.HTTP_403_FORBIDDEN),
            (self.issue_client, status.HTTP_400_BAD_REQUEST),
            (self.contributor_client, status.HTTP_400_BAD_REQUEST),
        ]
        for client, expected_status in clients_and_responses:
            response: Response = client.post(reverse("issue-list"), issue_data)
            self.assertEqual(response.status_code, expected_status)
            if expected_status == status.HTTP_400_BAD_REQUEST:
                self.assertEqual(response.data["assign_to"], ["Assignee must be a contributor of the project."])


class CommentViewSetTestCase(TestCase):
    def setUp(self):
        self.anonymous_client = APIClient()
        self.noperm_client = APIClient()
        self.noperm_user: SoftUser = SoftUser.objects.create(
            username="no_perm_user",
            email="noperm@mail.com",
            password="nopermpassword",
            birthdate="2022-02-02",
        )
        self.noperm_client.force_authenticate(user=self.noperm_user)
        self.comment_user: SoftUser = SoftUser.objects.create(
            username="commenttestuser",
            email="test@mail.com",
            password="testpassword",
            birthdate="2020-01-01",
        )
        self.comment_client = APIClient()
        self.comment_client.force_authenticate(user=self.comment_user)
        self.project = Project.objects.create(
            name="Test Project",
            description="Test Description",
            author=self.comment_user,
            type="BAE",
        )
        self.issue = Issue.objects.create(
            name="Test Issue",
            description="Test Description",
            tag="BUG",
            priority="HIG",
            project=self.project,
            author=self.comment_user,
            assign_to=self.comment_user,
        )
        self.comment = Comment.objects.create(
            content="Test Comment",
            author=self.comment_user,
            issue=self.issue,
        )
        self.contributor_client = APIClient()
        self.contributor = SoftUser.objects.create(
            username="contributor",
            email="contributor@mail.com",
            password="contributorpassword",
            birthdate="2000-01-01",
        )
        self.project.contributors.add(self.contributor)
        self.contributor_client.force_authenticate(user=self.contributor)

    def test_anonymous_user_cannot_access_comment(self):
        response: Response = self.anonymous_client.get(reverse("comment-detail", args=[self.comment.pk]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_only_contributor_and_comment_user_can_access_comment(self):
        clients_and_responses: list[tuple[APIClient, int]] = [
            (self.anonymous_client, status.HTTP_401_UNAUTHORIZED),
            (self.noperm_client, status.HTTP_403_FORBIDDEN),
            (self.comment_client, status.HTTP_200_OK),
            (self.contributor_client, status.HTTP_200_OK),
        ]
        for client, expected_status in clients_and_responses:
            response: Response = client.get(reverse("comment-detail", args=[self.comment.pk]))
            self.assertEqual(response.status_code, expected_status)

    def test_comment_creation(self):
        comment_data = {
            "content": "New Comment",
            "author": self.contributor.pk,
            "issue": self.issue.pk,
        }
        clients_and_responses: list[tuple[APIClient, int]] = [
            (self.anonymous_client, status.HTTP_401_UNAUTHORIZED),
            (self.noperm_client, status.HTTP_403_FORBIDDEN),
            (self.comment_client, status.HTTP_201_CREATED),
            (self.contributor_client, status.HTTP_201_CREATED),
        ]
        comment_number_to_create = 0
        initial_comment_count = Comment.objects.count()
        for client, expected_status in clients_and_responses:
            comment_data["content"] = f"New Comment {comment_number_to_create}"
            response: Response = client.post(reverse("comment-list"), comment_data)
            self.assertEqual(response.status_code, expected_status)
            comment_number_to_create += 1
            current_comment_count = Comment.objects.count()
            if expected_status == status.HTTP_201_CREATED:
                self.assertEqual(current_comment_count, initial_comment_count + 1)
                initial_comment_count += 1
            else:
                self.assertEqual(current_comment_count, initial_comment_count)

    def test_only_comment_user_can_edit_comment(self):
        original_comment_content = self.comment.content
        clients_and_responses: list[tuple[APIClient, int]] = [
            (self.anonymous_client, status.HTTP_401_UNAUTHORIZED),
            (self.noperm_client, status.HTTP_403_FORBIDDEN),
            (self.contributor_client, status.HTTP_403_FORBIDDEN),
            (self.comment_client, status.HTTP_200_OK),
        ]
        for client, expected_status in clients_and_responses:
            response: Response = client.patch(reverse("comment-detail", args=[self.comment.pk]), {"content": "New Content"})
            self.assertEqual(response.status_code, expected_status)
            self.comment.refresh_from_db()
            self.assertEqual(
                self.comment.content,
                original_comment_content if client != self.comment_client else "New Content",
            )

    def test_only_comment_user_can_delete_comment(self):
        clients_and_responses: list[tuple[APIClient, int]] = [
            (self.anonymous_client, status.HTTP_401_UNAUTHORIZED),
            (self.noperm_client, status.HTTP_403_FORBIDDEN),
            (self.contributor_client, status.HTTP_403_FORBIDDEN),
            (self.comment_client, status.HTTP_204_NO_CONTENT),
        ]
        for client, expected_status in clients_and_responses:
            response: Response = client.delete(reverse("comment-detail", args=[self.comment.pk]))
            self.assertEqual(response.status_code, expected_status)
