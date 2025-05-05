import asyncio
import queue
import time
from typing import Callable, Any, Optional, Type, TypeVar, ParamSpec

import loguru

from config.ConfigContainer import ConfigContainer

T = TypeVar('T')  # Return type
P = ParamSpec('P')
class TaskScheduler:
    """
    An asynchronous task scheduler using asyncio.

    This class provides a way to run tasks concurrently using asyncio tasks.
    It supports tasks that return a value and tasks that do not.
    """

    def __init__(self, config: ConfigContainer, num_workers: int = 5, task_name_prefix: str = "AsyncTaskSchedulerTask"):
        """
        Initialize the TaskScheduler.

        Args:
            num_workers: The number of worker tasks.
            task_name_prefix: The prefix for the names of the tasks created.
        """
        self.config = config

        if num_workers <= 0:
            raise ValueError("num_workers must be greater than 0")
        
        self._num_workers = num_workers
        self._task_name_prefix = task_name_prefix
        self._task_queue = asyncio.Queue()
        self._running_tasks = set()
        self._is_shutdown = False
        self._worker_tasks = []

    async def start(self):
        """Start the worker tasks."""
        if self._worker_tasks:
            return  # Already started
        for i in range(self._num_workers):
            worker_task = asyncio.create_task(self._worker(i), name=f"{self._task_name_prefix}-{i}")
            self._worker_tasks.append(worker_task)

    async def _worker(self, worker_id: int):
        """
        A worker task that processes tasks from the queue.
        """
        while not self._is_shutdown:
            try:
                func, args, kwargs, future = await self._task_queue.get()
                if func is None:  # Shutdown signal
                    self._task_queue.task_done()
                    break
                try:
                    if future:
                        result = await func(*args, **kwargs)
                        future.set_result(result)
                    else:
                        await func(*args, **kwargs)  # Await the function
                except Exception as e:
                    if future:
                        future.set_exception(e)
                    else:
                        loguru.logger.debug(f"Task in worker {worker_id} raised an exception: {e}") # Log if no future
                finally:
                    self._task_queue.task_done()
                # loguru.logger.debug(f"Worker {worker_id} processed task {func.__name__}") # Removed excessive logging
            except asyncio.CancelledError:
                loguru.logger.debug(f"Worker {worker_id} cancelled")
                break  # Exit the loop on cancellation

    async def submit(self, func: Callable[P, None], *args: P.args, **kwargs: P.kwargs) -> None:
        """
        Submit a task to the scheduler that does not return a value.

        Args:
            func: The callable (function) to execute.  Must be a coroutine function.
            *args: Positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.

        Raises:
            RuntimeError: If the scheduler has been shut down.
        """
        if self._is_shutdown:
            raise RuntimeError("Cannot submit tasks after shutdown")
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("func must be a coroutine function")

        await self._task_queue.put((func, args, kwargs, None))

    async def submit_with_return(self, func: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> asyncio.Future[T]:
        """
        Submit a task to the scheduler that returns a value.

        Args:
            func: The callable (function) to execute. Must be a coroutine function.
            *args: Positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.

        Returns:
            An asyncio.Future object representing the result of the task.

        Raises:
            RuntimeError: If the scheduler has been shut down.
        """
        if self._is_shutdown:
            raise RuntimeError("Cannot submit tasks after shutdown")
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("func must be a coroutine function")

        future = asyncio.get_event_loop().create_future()
        await self._task_queue.put((func, args, kwargs, future))
        return future

    async def shutdown(self, wait: bool = True) -> None:
        """
        Shut down the scheduler.

        Args:
            wait: If True, wait for all running tasks to complete before shutting
                  down the worker tasks. If False, the worker tasks will be cancelled immediately.
        """
        if self._is_shutdown:
            return
        self._is_shutdown = True

        if wait:
            # Signal workers to exit and wait for them to finish.
            for _ in range(self._num_workers):
                await self._task_queue.put((None, (), {}, None))  # Signal workers to shutdown
            await asyncio.gather(*self._worker_tasks, return_exceptions=True) # Wait, and get exceptions
        else:
            for worker_task in self._worker_tasks:
                worker_task.cancel()  # Cancel the worker tasks
            await asyncio.gather(*self._worker_tasks, return_exceptions=True) #  wait for cancellation
        self._worker_tasks.clear()

    async def __aenter__(self) -> 'TaskScheduler':
        """Async context manager enter."""
        await self.start()
        return self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[Any]):
        """Async context manager exit."""
        await self.shutdown(wait=True)

    async def get_running_tasks_count(self) -> int:
        """
        Get the number of currently running tasks.  This is an approximation.

        Returns:
            The number of tasks that are currently being executed by the scheduler.
        """
        return self._task_queue.qsize + len(self._running_tasks) #  Approximation

    def is_shutdown(self) -> bool:
        """
        Check if the scheduler has been shut down.

        Returns:
            True if the scheduler has been shut down, False otherwise.
        """
        return self._is_shutdown