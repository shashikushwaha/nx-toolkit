# NXKit

> Pythonic NX automation built on top of Siemens NXOpen.

NXKit is an open-source Python framework that simplifies automation and customisation in Siemens NX.

Built on top of the NX Open API, NXKit provides a clean, intuitive, and productivity-focused interface that helps engineers and developers automate NX workflows without dealing with the complexity of native NXOpen programming.

Instead of spending time creating builders, navigating object collections, and managing repetitive API patterns, you can focus on solving engineering problems and building robust automation solutions.

---

## Why NXKit?

NXOpen is incredibly powerful, but even simple operations often require a large amount of boilerplate code.

### NXOpen

```python
session = NXOpen.Session.GetSession()
work_part = session.Parts.Work

for body in work_part.Bodies:
    print(body.Name)
```

### NXKit

```python
import nxkit as nx

part = nx.active_part()

for body in part.bodies():
    print(body.name)
```

NXKit reduces complexity while preserving access to the full capabilities of NXOpen.

---

## Key Features

- Clean and Pythonic API design
- High-level wrappers around NXOpen objects
- Simplified session and part management
- Geometry abstraction layer
- Interactive selection utilities
- Assembly management tools
- Expression and attribute helpers
- User interface utilities
- Extensible plugin architecture
- Designed for engineers and automation developers

---

## Design Philosophy

### Pythonic

NXKit should feel natural to Python developers.

```python
body.name
body.volume
part.save()
```

instead of:

```python
body.Name
body.GetMassProperties()
part.Save()
```

### Workflow-Oriented

Focus on engineering workflows rather than NXOpen implementation details.

```python
part.extrude(sketch, distance=25)
```

instead of manually creating and managing builders.

### Productivity First

Reduce boilerplate and improve script readability.

### Extensible

Build a foundation for larger automation frameworks, custom applications, and reusable engineering tools.

---

## Installation

```bash
pip install nxkit
```

---

## Requirements

### Siemens NX Required

NXKit is a wrapper around Siemens NXOpen and requires:

- Siemens NX installation
- Valid Siemens NX license
- NX Open Python environment

> **Important**
>
> NXKit does not replace Siemens NX and does not contain any Siemens NX functionality itself.
>
> The library communicates with the NX Open API provided by Siemens NX. Without a licensed NX installation, NXKit cannot access NX models, assemblies, drawings, or geometry data.

### Architecture

```text
Your Python Script
        │
        ▼
    NXKit
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

### Access the Active Part

```python
import nxkit as nx

part = nx.active_part()

print(part.name)
```

### List All Bodies

```python
import nxkit as nx

part = nx.active_part()

for body in part.bodies():
    print(body.name)
```

### Select a Face

```python
face = nx.select_face()

print(face.area)
```

### Save the Part

```python
part.save()
```

---

## Example

```python
import nxkit as nx

part = nx.active_part()

body = nx.select_body()

print(f"Name: {body.name}")
print(f"Volume: {body.volume}")

body.rename("MAIN_BODY")

part.save()

nx.message("Operation completed.")
```

---

## Planned Package Structure

```text
nxkit/
│
├── session
├── geometry
├── sketches
├── features
├── assemblies
├── drafting
├── selection
├── ui
├── utils
└── constants
```

Future expansions:

```text
nxkit.cam
nxkit.cae
nxkit.sheetmetal
nxkit.measure
nxkit.pdm
```

---

## Documentation

Comprehensive documentation is available in the Wiki.

### Recommended Reading

- Getting Started
- Installation
- Session API
- Part API
- Geometry API
- Selection API
- Sketch API
- Feature API
- Assembly API
- Examples

---

## Contributing

Contributions are welcome.

Whether you are fixing bugs, improving documentation, proposing new APIs, or creating new wrappers around NXOpen functionality, your help is greatly appreciated.

Please read the Contributing Guide before submitting a pull request.

---

## Roadmap

### v0.1

- Session management
- Part wrappers
- Body wrappers
- Face wrappers
- Edge wrappers
- Selection utilities
- UI helpers

### v0.2

- Sketch API
- Feature API
- Expressions
- Attribute management

### v1.0

- Stable public API
- Assembly management
- Drafting support
- Plugin architecture
- Extended documentation

---

## Disclaimer

NXKit is an independent open-source project and is not affiliated with, endorsed by, or maintained by Siemens Digital Industries Software.

Siemens NX and NX Open are trademarks of Siemens Digital Industries Software or their respective owners.

---

## Vision

NXKit aims to become the easiest and most productive way to automate Siemens NX with Python.

Our mission is simple:

> Focus on engineering problems, not NXOpen boilerplate.

---

## License

Distributed under the MIT License.

See the `LICENSE` file for more information.

---

# Write less NXOpen. Build more with NXKit.
