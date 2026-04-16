FROM python:3.12-slim

# Qt runtime libraries for PySide6, plus xvfb for headless display during tests.
# --no-install-recommends keeps the image lean; we clean the apt lists in the
# same layer so they don't bloat the final image.
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb \
    libglib2.0-0 \
    libxkbcommon-x11-0 libxkbcommon0 \
    libxcb-cursor0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 \
    libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxcb-sync1 \
    libxcb-xfixes0 libxcb-xkb1 \
    libegl1 libopengl0 libpulse0 libdbus-1-3 libfontconfig1 \
    libgssapi-krb5-2 \
    && rm -rf /var/lib/apt/lists/*

# Install uv once - it's used by both the build-time install and the entrypoint.
RUN pip install --no-cache-dir --upgrade pip uv

WORKDIR /app

# Copy dependency metadata first so Docker can cache the pip install layer.
# Changes to source files (.py) won't invalidate this layer - only changes to
# pyproject.toml or setup.py will trigger a re-install.
COPY pyproject.toml setup.py ./

# Install project dependencies. `|| true` lets this succeed even though the
# source isn't copied yet; the real install happens after the full COPY below.
RUN uv pip install --system --no-cache -e ".[tests]" || true

# Now copy the rest of the source. Edits to .py files invalidate only this
# layer and everything below it - not the heavy pip install layer above.
COPY . .

# Re-run the install to register the package itself. Dependencies are already
# satisfied from the layer above, so this is fast.
RUN uv pip install --system --no-cache -e ".[tests]"

# Install entrypoint while still root so chmod works predictably.
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Drop to a non-root user for actually running the app. UID 1000 matches the
# typical host user so bind-mounted files stay writable from the host.
RUN useradd -m -u 1000 app && chown -R app:app /app
USER app

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]