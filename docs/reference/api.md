---
title: API Reference
description: Python API documentation
audience:
  - users
  - contributors
tags:
  - reference
  - api
---

# API Reference

Python API documentation for pynetappfoundry.

## Core Classes

### Config

Configuration management for cluster connections.

::: pynetappfoundry.core.config.Config
    options:
      show_root_heading: true
      show_source: false

### setup_logger

Logging configuration.

::: pynetappfoundry.core.logging.setup_logger
    options:
      show_root_heading: true
      show_source: false

## ONTAP Clients

### ONTAPAPIClient

REST API client for ONTAP clusters.

::: pynetappfoundry.clients.ontap.api.ONTAPAPIClient
    options:
      show_root_heading: true
      show_source: false

### ONTAPCLI

SSH CLI client for ONTAP clusters.

::: pynetappfoundry.clients.ontap.cli.ONTAPCLI
    options:
      show_root_heading: true
      show_source: false

### CLICommandError

Exception raised when CLI commands fail.

::: pynetappfoundry.clients.ontap.cli.CLICommandError
    options:
      show_root_heading: true
      show_source: false

## Database Classes

### MetricDB

Database for storing cluster metrics.

::: pynetappfoundry.db.metrics.MetricDB
    options:
      show_root_heading: true
      show_source: false

### EmsEventsDB

Database for storing EMS events.

::: pynetappfoundry.db.ems.EmsEventsDB
    options:
      show_root_heading: true
      show_source: false

### AzEventsDB

Database for storing Azure events.

::: pynetappfoundry.db.azevents.AzEventsDB
    options:
      show_root_heading: true
      show_source: false

## Utility Classes

### APIWrapper

Generic OpenAPI wrapper for REST APIs.

::: pynetappfoundry.clients.openapi.APIWrapper
    options:
      show_root_heading: true
      show_source: false

### DIIAPIClient

DII API client.

::: pynetappfoundry.clients.dii.api.DIIAPIClient
    options:
      show_root_heading: true
      show_source: false

## Module Structure

```
pynetappfoundry/
├── __init__.py          # Package exports
├── _version.py          # Version (generated)
├── cli.py               # Click CLI entry point
├── core/
│   ├── config.py        # Configuration management
│   └── logging.py       # Logging setup
├── clients/
│   ├── openapi.py       # Generic API wrapper
│   ├── ontap/
│   │   ├── api.py       # REST API client
│   │   └── cli.py       # SSH CLI client
│   └── dii/
│       └── api.py       # DII API client
└── db/
    ├── metrics.py       # Metrics database
    ├── ems.py           # EMS events database
    └── azevents.py      # Azure events database
```
