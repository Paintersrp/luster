import re
from typing import Dict, Any, List, Type, Tuple

from auditlog.models import LogEntry
from django.shortcuts import get_object_or_404
from django.db.models import ForeignKey, ManyToManyField, Model, ImageField, QuerySet
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse, NoReverseMatch
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from authorization.models import User


class SyView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    """
    A custom view that combines list, create, retrieve, update, and destroy operations.
    """

    serializer_class: Type[Serializer] = None
    model_class: Type[Model] = None
    fk_fields: List[str] = []
    mtm_fields: Dict[str, str] = {}
    mtm_values: Dict[str, List[Any]] = {}

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle GET requests.

        Args:
            request (Request): The request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response.
        """

        if "pk" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def create(self, request) -> Response:
        """
        Handle POST requests for object creation.

        Args:
            request (Request): The request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response.
        """

        data = request.data.copy()
        model_fields = self.serializer_class.Meta.model._meta.get_fields()
        self.pre_process_fields(request, data, model_fields, False)

        serializer = self.model_class.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)

        self.update_instance_mtm_fields(instance)
        self.log_entry(request, instance, None, "create")

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request) -> Response:
        """
        Handle PUT requests for object update.

        Args:
            request (Request): The request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response.
        """

        instance = self.get_object()
        old_instance = self.model_class.objects.get(pk=instance.pk)
        model_fields = self.serializer_class.Meta.model._meta.get_fields()

        data = self.check_data_for_images(instance, request)
        self.pre_process_fields(request, data, model_fields, True)
        serializer = self.get_serializer(instance, data=data, partial=True)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        self.update_instance_mtm_fields(instance)
        self.log_entry(request, instance, old_instance, "update")

        return Response(serializer.data)

    def destroy(self, request) -> Response:
        """
        Handle DELETE requests for object deletion.

        Args:
            request (Request): The request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response.
        """

        instance = self.get_object()
        if hasattr(instance, "image") and instance.image is not None:
            instance.image.delete()

        self.perform_destroy(instance)
        self.log_entry(request, instance, None, "delete")

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self) -> QuerySet:
        """
        Get the queryset for the view.

        Returns:
            QuerySet: The queryset for the view.
        """

        return self.model_class.objects.all()

    def perform_create(self, serializer: Serializer) -> None:
        """
        Perform create operation using the serializer.

        Args:
            serializer (Serializer): The serializer instance.
        """

        return serializer.save()

    def get_object(self) -> Model:
        """
        Retrieve the object based on the given lookup parameters.

        Returns:
            Model: The retrieved object.

        Raises:
            Http404: If the object does not exist.
        """

        pk = self.kwargs.get("pk")
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def pre_process_fields(
        self,
        request,
        data: Dict[str, Any],
        model_fields: List[Any],
        update: bool = False,
    ) -> None:
        """
        Pre-process the fields in the request data.

        Args:
            request (HttpRequest): The request object.
            data (Dict[str, Any]): The request data.
            model_fields: The model fields.
            update (bool): Indicates whether it's an update operation.
        """

        if self.fk_fields:
            self.process_foreign_key_fields(data, update)

        if self.mtm_fields:
            self.process_many_to_many_fields(data, model_fields)

        if any(field.name == "author" for field in model_fields):
            self.process_author_field(request, data)

    def update_instance_mtm_fields(self, instance) -> None:
        """
        Update the ManyToMany fields of the instance.

        Args:
            instance: The instance object.
        """

        for field in self.mtm_values:
            instance_field = getattr(instance, field)
            instance_field.set(self.mtm_values[field])

    def log_entry(
        self,
        request,
        instance,
        old_instance,
        type="create",
    ) -> None:
        """
        Log the entry for the instance.

        Args:
            request (HttpRequest): The request object.
            instance: The instance object.
            old_instance: The old instance object.
            type (str): The type of action ("create", "update", "delete").
        """

        change_str = (
            self.return_changes(instance, old_instance) if type == "update" else None
        )

        action = (
            LogEntry.Action.UPDATE
            if type == "update"
            else LogEntry.Action.CREATE
            if type == "create"
            else LogEntry.Action.DELETE
        )

        self.__create_log_entry(
            action,
            request.username if request.username else None,
            instance,
            change_str,
        )

    def __create_log_entry(
        self, action: str, username: str, instance: Model, changes: str
    ) -> None:
        """
        Create a log entry for the given action, username, instance, and changes.

        Args:
            action (str): The action performed.
            username (str): The username.
            instance (models.Model): The instance.
            changes (str): The changes made.

        """

        content_type = ContentType.objects.get_for_model(instance)

        if not changes:
            changes = ""

        log_entry = LogEntry(
            content_type=content_type,
            object_id=instance.pk,
            object_repr=str(instance),
            action=action,
            actor=username,
            changes=changes,
            timestamp=timezone.now(),
        )
        log_entry.save()

    def return_changes(self, instance: Model, old_instance: Model) -> str:
        """
        Return the changes made between the instance and the old instance.

        Args:
            instance (models.Model): The current instance.
            old_instance (models.Model): The old instance.

        Returns:
            str: The formatted change message string.

        """

        changes: Dict[str, Tuple[str, str]] = {}

        for field in instance._meta.fields:
            field_name = field.name
            if str(getattr(instance, field_name)) != str(
                getattr(old_instance, field_name)
            ):
                changes[field_name] = [
                    getattr(old_instance, field_name),
                    getattr(instance, field_name),
                ]

        change_message_str: str = ""
        num_changes = len(changes)

        for i, (field, values) in enumerate(changes.items()):
            old_value, new_value = values
            change_message_str += f"{field}: {old_value} -> {new_value}"
            if i < num_changes - 1:
                change_message_str += ", "

        return change_message_str

    def process_foreign_key_fields(
        self,
        data: Dict[str, Any],
        update: bool = False,
    ) -> None:
        """
        Process foreign key fields in the request data.

        Args:
            data (Dict): The request data.

        Raises:
            NotFound: If the related object is not found.
        """

        for field in self.fk_fields:
            if field in data:
                related_class = self.serializer_class.Meta.model._meta.get_field(
                    field
                ).remote_field.model

                try:
                    related_obj = related_class.objects.get(id=data[field])
                except related_class.DoesNotExist:
                    raise NotFound(
                        detail=f"{related_class.__name__} with id {data[field]} does not exist"
                    )

                data[f"{field}"] = related_obj.id

                if update:
                    instance = self.get_object()
                    setattr(instance, field, related_obj)

    def process_many_to_many_fields(
        self,
        data: Dict[str, Any],
        model_fields: List[Any],
    ) -> None:
        """
        Process many-to-many fields in the request data.

        Args:
            data (Dict): The request data.
            model_fields (List[Field]): The model fields.

        Raises:
            NotFound: If the related object is not found.
        """

        model_fields = self.serializer_class.Meta.model._meta.get_fields()

        self.mtm_fields = {
            field.name: ""
            for field in model_fields
            if isinstance(field, ManyToManyField)
        }

        for field in model_fields:
            if isinstance(field, ForeignKey) and field.name == "tag":
                related_class = field.remote_field.model
                if "tag" in data and not data["tag"].isnumeric():
                    tag = data.pop("tag", None)
                    tag_obj, created = related_class.objects.get_or_create(name=tag[0])
                    data["tag"] = tag_obj.id

            elif isinstance(field, ForeignKey):
                related_class = field.remote_field.model

                if field.name in data:
                    obj = data.pop(field.name, None)
                    foo_obj, created = related_class.objects.get_or_create(id=obj[0])
                    data[field.name] = foo_obj.id

            elif isinstance(field, ManyToManyField):
                self.mtm_fields[field.name] = field.remote_field.model

        self.mtm_values = {
            field.name: []
            for field in model_fields
            if isinstance(field, ManyToManyField)
        }

        pop_keys = []

        for key, value in data.items():
            parts = re.findall(r"\[(.*?)\]", key)
            name = key.split("[")[0]

            if name in self.mtm_fields:
                if len(parts) == 2 and parts[0].isdigit() and parts[1] == "id":
                    element_obj, created = self.mtm_fields[name].objects.get_or_create(
                        id=value
                    )
                    self.mtm_values[name].append(element_obj)

                pop_keys.append(key)

        for key in pop_keys:
            data.pop(key, None)

    def process_author_field(
        self,
        request,
        data: Dict[str, Any],
    ) -> None:
        """
        Process the author field in the request data.

        Args:
            request (Request): The request object.
            data (Dict): The request data.
        """

        author = User.objects.get(username=request.username)
        data["author"] = author.id

    def check_data_for_images(self, instance, request) -> Dict[str, Any]:
        """
        Check the request data for image fields.

        Args:
            instance (Model): The instance object.
            request (Request): The request object.

        Returns:
            Dict: The updated request data.
        """

        image_field_name = None

        for field in instance._meta.fields:
            if isinstance(field, ImageField):
                image_field_name = field.name

        if image_field_name is not None:
            image = request.FILES.get(image_field_name)

            if image is None or image == getattr(instance, image_field_name):
                data = request.data.copy()
                data[image_field_name] = getattr(instance, image_field_name)
            else:
                getattr(instance, image_field_name).delete()

                data = request.data.copy()
        else:
            data = request.data.copy()

        return data


class SyBulkView(generics.DestroyAPIView, generics.UpdateAPIView):
    """
    A custom view that combines update and destroy bulk operations.
    """

    serializer_class = None
    model_class = None

    ids: List[int] = []

    def destroy(self, request, *args, **kwargs) -> None:
        """
        Delete multiple objects based on provided ids.

        Args:
            request: The request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response.

        """
        self.ids: List[int] = request.data.get("ids", [])

        if not self.ids:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(id__in=self.ids)

        for obj in queryset:
            if hasattr(obj, "image") and obj.image is not None:
                obj.image.delete()

        deleted = queryset.delete()

        if self.model_class.__name__ == "Messages":
            unread_queryset = self.filter_queryset(self.get_queryset())
            unread_queryset = unread_queryset.filter(is_read=False)
            count = unread_queryset.count()

            return Response({"count": count}, status=status.HTTP_200_OK)

        if deleted[0] == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs) -> Response:
        """
        Handle PUT requests for object update.

        Args:
            request (Request): The request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response.
        """

        self.ids: List[int] = request.data.get("ids", [])

        if not self.ids:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        field = request.data.get("field")
        value = request.data.get("value")

        if not field or value is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(id__in=self.ids)

        if field[0] == "is_archived":
            updated = queryset.update(**{field[0]: value, "is_read": True})

        if field[0] == "is_read" and value == True:
            updated = queryset.update(**{field[0]: value})
            unread_queryset = self.filter_queryset(self.get_queryset())
            unread_queryset = unread_queryset.filter(is_read=False)
            count = unread_queryset.count()

            return Response({"count": count}, status=status.HTTP_200_OK)

        elif field[0] == "is_read" and value == False:
            updated = queryset.update(**{field[0]: value, "is_archived": False})
            unread_queryset = self.filter_queryset(self.get_queryset())
            unread_queryset = unread_queryset.filter(is_read=False)
            count = unread_queryset.count()

            return Response({"count": count}, status=status.HTTP_200_OK)

        if updated == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)


class SyMetaView(APIView):
    """
    A custom view for processing metadata.
    """

    def analyze_app(models: List[Model]) -> Dict[str, any]:
        """
        Analyze an app and provide statistics about its models.

        Parameters:
            models (List[Model]): The list of Django models to analyze.

        Returns:
            Dict[str, any]: A dictionary containing various statistics about the app's models.
        """

        num_models = 0
        num_objects = 0
        model_stats = []

        for model in models:
            model_stats.append(
                {
                    "name": model._meta.verbose_name,
                    "icon": model._meta.icon,
                    "related_components": model._meta.related_components,
                    "related_components_count": len(model._meta.related_components),
                    "num_objects": model.objects.count(),
                    "visibility": model._meta.visibility,
                }
            )
            num_models += 1
            num_objects += model.objects.count()

        return {
            "num_models": num_models,
            "num_objects": num_objects,
            "models": model_stats,
        }

    def process_app(
        self, app_label: str, app_config: Any, endpoints: Dict[str, Any]
    ) -> None:
        """
        Process the app configuration and update the endpoints dictionary.

        Args:
            app_label (str): The label of the app.
            app_config (Any): The configuration of the app.
            endpoints (Dict[str, Any]): The endpoints dictionary to update.
        """

        endpoints["configs"][app_label] = {
            "icon": app_config.icon if hasattr(app_config, "icon") else None,
            "links": app_config.links if hasattr(app_config, "links") else None,
            "visibility": app_config.visibility
            if hasattr(app_config, "visibility")
            else None,
        }
        endpoints["models"][app_label] = []

    def process_model(self, model: Model, serializer_class: Any) -> Dict[str, Any]:
        """
        Process the model and serializer to create the endpoint dictionary.

        Args:
            model (Any): The model to process.
            serializer_class (Any): The serializer class for the model.

        Returns:
            Dict[str, Any]: The endpoint dictionary.
        """

        model_name = model.__name__.lower()

        serializer = serializer_class()
        fields = serializer.get_fields()
        metadata = {}

        for field_name, field in fields.items():
            if not field_name == "id":
                metadata[field_name] = {"type": field.__class__.__name__}

                try:
                    if model._meta.get_field(field_name).verbose_name:
                        metadata[field_name]["verbose_name"] = model._meta.get_field(
                            field_name
                        ).verbose_name
                except:
                    metadata[field_name]["verbose_name"] = None

        if "alignment" in metadata:
            metadata["alignment"]["choices"] = dict(model.ALIGNMENT_CHOICES)

        try:
            url = reverse(f"{model_name}-list")
            url = url.replace("/api/", "/")
        except NoReverseMatch:
            url = None

        endpoint = {
            "app_name": model._meta.app_label,
            "model_name": model_name,
            "verbose_name": model._meta.verbose_name,
            "verbose_name_plural": model._meta.verbose_name_plural,
            "url": url,
            "metadata": metadata,
            "keys": serializer.FIELD_KEYS,
            "autoFormLabel": model._meta.autoform_label
            if hasattr(model._meta, "autoform_label")
            else None,
            "longDescription": model._meta.long_description
            if hasattr(model._meta, "long_description")
            else None,
            "shortDescription": model._meta.short_description
            if hasattr(model._meta, "short_description")
            else None,
            "pagesAssociated": model._meta.pages_associated
            if hasattr(model._meta, "pages_associated")
            else None,
            "preview": model._meta.include_preview
            if hasattr(model._meta, "include_preview")
            else False,
            "icon": model._meta.icon if hasattr(model._meta, "icon") else None,
            "icon_class": model._meta.icon_class
            if hasattr(model._meta, "icon_class")
            else None,
            "slug": model._meta.slug if hasattr(model._meta, "slug") else None,
            "tags": model._meta.tags if hasattr(model._meta, "tags") else False,
            "relatedComponents": model._meta.related_components
            if hasattr(model._meta, "related_components")
            else None,
            "visibility": model._meta.visibility
            if hasattr(model._meta, "visibility")
            else None,
            "access_level": model._meta.access_level
            if hasattr(model._meta, "access_level")
            else None,
            "info_dump": model._meta.info_dump
            if hasattr(model._meta, "info_dump")
            else None,
        }

        if hasattr(serializer, "SEARCH_KEYS"):
            endpoint["search_keys"] = serializer.SEARCH_KEYS

        return endpoint
