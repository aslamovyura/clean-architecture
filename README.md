# clean-architecture


## DB migrations

Run the following command to automatically detect DB changes and generate pending migration:
    ```shell
    alembic revision --autogenerate -m "Initial Create"
    ```

Then, apply the migrations:
    ```shell
    alembic upgrade head
    ```