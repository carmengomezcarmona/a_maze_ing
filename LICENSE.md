MIT License

Copyright (c) 2026 carmgome, gapostig

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

---

Why MIT for this project:

`mazegen` is explicitly designed to be reused as a standalone dependency by
future 42 projects (per the subject's "Code reusability requirements").
MIT was chosen because it:

- Explicitly permits reuse, modification and redistribution (including in
  closed-source or graded projects), which is a hard requirement here.
- Has no "copyleft" clause, so any later project that installs
  `mazegen-*.whl` is never forced to adopt a particular license itself.
- Is short, well understood, and standard for small reusable Python
  packages, avoiding ambiguity for whoever picks this up next.
