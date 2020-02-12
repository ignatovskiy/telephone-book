FROM python:3

WORKDIR .

COPY . .

ENV DISPLAY: .0

CMD [ "python", "./telephone_book.py" ]