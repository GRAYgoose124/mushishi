FROM python:3 as build
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl https://install.python-poetry.org/ | python -
WORKDIR /app
COPY . .
RUN poetry install --no-interaction --no-ansi -vvv

FROM python:3-slim as runtime
ENV PYTHONUNBUFFERED=true
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=build /app /app
CMD ["mushishi"]