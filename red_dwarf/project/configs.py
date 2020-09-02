import os
from typing import Dict, List
from datetime import datetime
from red_dwarf.project.enums import ExecutionIntervals, ExecutionMethods


class TableConfig:

    def __init__(self, schema: str, name: str) -> None:
        self.schema = schema
        self.name = name
        self._column_list: List[str] = None

    @property
    def column_list(self) -> List[str]:
        return self._column_list

    @column_list.setter
    def column_list(self, value):
        self._column_list = value


class ExecutionConfig:

    def __init__(self, **kwargs) -> None:
        self._method: ExecutionMethods = kwargs.get('method')
        self._interval: str = kwargs.get('interval')
        self._start_date: datetime = kwargs.get('start_date')
        self._interval_value: int = kwargs.get('interval_value')

    @classmethod
    def new_once(cls, method: ExecutionMethods, start_date: datetime):
        return cls(method=method, start_date=start_date)

    @classmethod
    def new_incremental(cls, method: ExecutionMethods, interval: str, interval_value: int):
        return cls(method=method, interval=interval, interval_value=interval_value)

    @classmethod
    def new_once_incremental(cls,
                             method: ExecutionMethods,
                             start_date: datetime,
                             interval: str,
                             interval_value: int):

        return cls(method=method, start_date=start_date, interval=interval, interval_value=interval_value)

    @classmethod
    def new(cls, **kwargs):

        try:
            method = ExecutionMethods[kwargs['method']]

        except KeyError:
            raise KeyError(f"the execution and method options must be set in the red-dwarf config")

        except ValueError:
            raise ValueError(
                f"Invalid value set for execution method, options are {ExecutionMethods.members()}")

        if method == ExecutionMethods.ONCE:
            return cls.new_once(**kwargs)

        elif method == ExecutionMethods.INCREMENTAL:
            return cls.new_incremental(**kwargs)

        elif method == ExecutionMethods.ONCE_INCREMENTAL:
            return cls.new_once_incremental(**kwargs)

        else:
            raise ValueError("Invalid execution config. Please fix it and try again.")

    @property
    def method(self) -> ExecutionMethods:
        return ExecutionMethods[self._method]

    @property
    def start_date(self) -> datetime:
        return self._start_date

    @property
    def interval(self) -> str:
        return self._interval

    @property
    def interval_value(self) -> int:
        return self._interval_value

    @property
    def once(self) -> str:
        if self.method == ExecutionMethods.ONCE or self.method == ExecutionMethods.ONCE_INCREMENTAL:
            return ExecutionMethods.ONCE.name
        else:
            return ''

    @property
    def incremental(self) -> str:
        if self.method == ExecutionMethods.INCREMENTAL or self.method == ExecutionMethods.ONCE_INCREMENTAL:
            return ExecutionMethods.INCREMENTAL.name
        else:
            return ''


class UnloadConfig:

    def __init__(self, vacuum: bool, delete: bool, analyse: bool, options: List[str]) -> None:
        self.vacuum = vacuum
        self.delete = delete
        self.analyse = analyse
        self.options = options

    @property
    def formatted_options(self) -> str:
        return '\n'.join(self.options)


class S3Config:

    def __init__(self, bucket: str, key_prefix: str, iam_role: str):
        self._bucket = bucket
        self._key_prefix = key_prefix
        self._iam_role = iam_role

    @property
    def bucket(self) -> str:
        return os.getenv(self._bucket, self._bucket)

    @property
    def key_prefix(self) -> str:
        return os.getenv(self._key_prefix, self._key_prefix)

    @property
    def iam_role(self) -> str:
        return os.getenv(self._iam_role, self._iam_role)


class PartitionConfig:

    def __init__(self, start_date: datetime, end_date: datetime, column: str, by: List[str]):
        self.start_date = start_date
        self.end_date = end_date
        self.column = column
        self._by = by

    @property
    def by(self) -> List[ExecutionIntervals]:
        return [ExecutionIntervals[x] for x in self._by]


class GlueConfig:

    def __init__(self, create_glue_catalog: bool, database: str, table_name: str) -> None:
        self.create_glue_catalog = create_glue_catalog
        self.database = database
        self.table_name = table_name


class SpectrumConfig:

    def __init__(self, create_external_table: bool, schema: str, table_name: str):
        self.create_external_table = create_external_table
        self.schema = schema
        self.table_name = table_name


class RedDwarfConfig:

    def __init__(self, table, execution, unload, glue, s3, spectrum, partition) -> None:
        self._table = TableConfig(**table)
        self._unload = UnloadConfig(**unload)
        self._execution = ExecutionConfig.new(**execution)
        self._glue = GlueConfig(**glue)
        self._s3 = S3Config(**s3)
        self._spectrum = SpectrumConfig(**spectrum)
        self.partition = PartitionConfig(**partition)

    @property
    def table(self) -> TableConfig:
        return self._table

    @property
    def unload(self) -> UnloadConfig:
        return self._unload

    @property
    def s3(self) -> S3Config:
        return self._s3

    @property
    def execution(self) -> ExecutionConfig:
        return self._execution
