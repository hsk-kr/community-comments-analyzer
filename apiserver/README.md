# apiserver

## How to start

1. Move to apiserver directory.
2. Install modules
    ```
    pip install requirements.txt
    ```
3. Run server
    ```
    python manage.py runserver
    ```

## APIS

### Get Comments between dates

Returns json data from es about comments.


|URL|URL Parameters|Sample Request|
|---|---|---|
|/api/v1/comments|Optional<br/>srt_date=[%Y-%m-%d]<br/>end_date=[%Y-%m-%d]|/api/v1/comments/srt_date=2020-02-15&end_date=2020-02-17

The default dates of srt_date and end_date are values of the django.utils.timezone.now function.