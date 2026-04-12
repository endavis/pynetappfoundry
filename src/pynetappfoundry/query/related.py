"""Relationship traversal between ONTAP resources.

Convenience functions that wrap :class:`~pynetappfoundry.query.queryset.QuerySet`
to express intent when fetching related resources (e.g., "all volumes for
this SVM").
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from pynetappfoundry.clients.openapi import APIWrapper
from pynetappfoundry.core.config import Config
from pynetappfoundry.query.queryset import QuerySet


def related[T: BaseModel](
    model_class: type[T],
    client: APIWrapper,
    *,
    config: Config,
    **kwargs: Any,
) -> list[Any]:
    """Fetch related ONTAP resources matching the given filters.

    A thin convenience wrapper over ``QuerySet.filter().all()`` that
    communicates relationship-traversal intent.

    Args:
        model_class: The target model class (must have a registered
            :class:`~pynetappfoundry.cache.field_mapping.TypeMapping`).
        client: An :class:`~pynetappfoundry.clients.openapi.APIWrapper`
            connected to the ONTAP cluster.
        config: A :class:`~pynetappfoundry.core.config.Config` instance
            used to construct the ``DataSource``.
        **kwargs: One or more filter keyword arguments using model attribute
            names (e.g. ``svm_uuid="abc-123"``).

    Returns:
        A list of model instances matching all filters.

    Raises:
        ValueError: If no filter kwargs are provided or if the model class
            has no registered TypeMapping.

    Example::

        from pynetappfoundry.query import related
        from pynetappfoundry.models.ontap.storage.volumes import OntapVolume

        vols = related(OntapVolume, client, config=config, svm_uuid="abc-123")
    """
    if not kwargs:
        msg = "related() requires at least one filter keyword argument."
        raise ValueError(msg)
    return QuerySet(model_class, client, config=config).filter(**kwargs).all()


def related_one[T: BaseModel](
    model_class: type[T],
    client: APIWrapper,
    *,
    config: Config,
    **kwargs: Any,
) -> Any | None:
    """Fetch a single related ONTAP resource, or ``None``.

    Same as :func:`related` but returns only the first result.  Useful for
    one-to-one relationships (e.g., "get the SVM for this volume").

    Args:
        model_class: The target model class.
        client: An :class:`~pynetappfoundry.clients.openapi.APIWrapper`
            connected to the ONTAP cluster.
        config: A :class:`~pynetappfoundry.core.config.Config` instance
            used to construct the ``DataSource``.
        **kwargs: One or more filter keyword arguments.

    Returns:
        A single model instance, or ``None`` if no match is found.

    Raises:
        ValueError: If no filter kwargs are provided or if the model class
            has no registered TypeMapping.

    Example::

        from pynetappfoundry.query import related_one
        from pynetappfoundry.models.ontap.svm.svms import OntapSvm

        svm = related_one(OntapSvm, client, config=config, uuid="svm-uuid-123")
    """
    if not kwargs:
        msg = "related_one() requires at least one filter keyword argument."
        raise ValueError(msg)
    return QuerySet(model_class, client, config=config).filter(**kwargs).first()
