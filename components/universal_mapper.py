from abc import ABCMeta, abstractmethod


class BaseMapper(metaclass=ABCMeta):
    def __init__(self, connection) -> None:
        self.connection = connection
        self.cursor = connection.cursor()

    @property
    @abstractmethod
    def tablename(self):
        pass

    @property
    @abstractmethod
    def model(self):
        pass

    def all(self):
        statement = f'SELECT * FROM {self.tablename}'
        self.cursor.execute(statement)
        column_names = [description_info[0] for description_info in
                        self.cursor.description]
        result = []

        for values in self.cursor.fetchall():
            object = self.model(**{column_names[i]: values[i]
                                   for i, _ in enumerate(values)})
            result.append(object)
        return result

    def insert(self, **schema):
        statement = f"INSERT INTO " \
                    f"{self.tablename} ({','.join(schema.keys())}) VALUES (?)"
        self.cursor.execute(statement, (','.join(schema.values()),))

        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, object, **schema):
        schema = {str(key) + '=?': value for key, value in schema.items()}
        statement = f'UPDATE {self.tablename}' \
                    f'SET {",".join(schema.keys())} WHERE id=?'
        self.cursor.execute(statement, (",".join(schema.values()), object.id))

        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, object):
        statement = f'DELETE FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (object.id,))

        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)

    def get_by_id(self, id):
        statement = f'SELECT * FROM {self.tablename} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()

        try:
            id, name = result
            return self.model(id=id, name=name)
        except Exception as e:
            raise RecordNotFoundException(f'Record with id={id} not found')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')
