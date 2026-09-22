# NXToolkit

> Pythonic NX automation built on top of Siemens NXOpen.

NXToolkit is a modern, high-level Python framework that simplifies automation and customisation in Siemens NX.

Built on top of the NX Open API, NXToolkit provides clean and intuitive abstractions that help engineers and developers create powerful NX automation tools without dealing with the complexity and boilerplate of native NXOpen programming.

Instead of spending time creating builders, managing sessions, and handling repetitive API patterns, you can focus on solving engineering problems and building automation workflows.

---

## Why NXToolkit?

NXOpen is extremely powerful, but common operations often require a significant amount of setup code.

### NXOpen

```python
session = NXOpen.Session.GetSession()
work_part = session.Parts.Work

for body in work_part.Bodies:
    print(body.Name)
```

### NXToolkit

```python
import nxtoolkit as nx

part = nx.active_part()

for body in part.bodies():
    print(body.name)
```

NXToolkit reduces complexity while maintaining full access to the underlying NX functionality.

---

## Features

- Pythonic API design
- High-level wrappers around NXOpen objects
- Simplified session and part management
- Easy geometry access and manipulation
- Interactive selection helpers
- Feature creation utilities
- Assembly automation tools
- UI and message box helpers
- Expression and attribute management
- Extensible architecture for CAM, CAE, and other NX applications

---

## Design Goals

NXToolkit is built around four principles:

### Simplicity

Reduce NXOpen boilerplate and expose concise APIs.

### Readability

Code should clearly express intent.

```python
body.rename("MAIN_BODY")

face.color("red")

part.save()
```

### Productivity

Automate common engineering tasks with minimal code.

### Extensibility

Provide a foundation for larger automation projects and custom workflows.

---

## Installation

```bash
pip install nxtoolkit
```

---

## Requirements

### Siemens NX Required

NXToolkit requires:

- Siemens NX installation
- Valid Siemens NX license
- NX Open Python environment

NXToolkit is a wrapper around NXOpen and does not replace Siemens NX.

Without a licensed Siemens NX installation, NXToolkit cannot access NX models, geometry, assemblies, drawings, or other NX functionality.

### Architecture

```text
Your Python Script
        │
        ▼
    NXToolkit
        │
        ▼
      NXOpen
        │
        ▼
    Siemens NX
        │
        ▼
    NX License
```

---

## Quick Start

### Access the active part

```python
import nxtoolkit as nx

part = nx.active_part()

print
