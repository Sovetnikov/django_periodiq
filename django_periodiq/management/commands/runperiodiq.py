import os
import sys

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.module_loading import module_has_submodule
from periodiq import entrypoint


class Command(BaseCommand):
    help = "Runs Periodiq process."

    def add_arguments(self, parser):
        parser.add_argument(
            "--path", "-P",
            default=".",
            nargs="*",
            type=str,
            help="The import path (default: .).",
        )
        parser.add_argument(
            "--pid-file",
            type=str,
            help="write the PID of the master process to a file (default: no pid file)",
        )
        parser.add_argument(
            "--log-file",
            type=str,
            help="write all logs to a file (default: sys.stderr)",
        )

    def handle(self, path, verbosity, pid_file, log_file, **options):
        executable_name = "periodiq"
        executable_path = self._resolve_executable(executable_name)
        verbosity_args = ["-v"] * (verbosity - 1)

        tasks_modules = self.discover_tasks_modules()
        process_args = [
            executable_name,
            # -v -v ...
            *verbosity_args,
            # django_dramatiq.tasks app1.tasks app2.tasks ...
            *tasks_modules,
            "--path", *path,
        ]

        if pid_file:
            process_args.extend(["--pid-file", pid_file])

        if log_file:
            process_args.extend(["--log-file", log_file])

        self.stdout.write(' * Running periodiq: "%s"\n\n' % " ".join(process_args))
        if os.name == 'nt':
            sys.argv = process_args
            entrypoint()
        else:
            os.execvp(executable_path, process_args)

    def discover_tasks_modules(self):
        ignored_modules = set(getattr(settings, "DRAMATIQ_IGNORED_MODULES", []))
        app_configs = (c for c in apps.get_app_configs() if module_has_submodule(c.module, "tasks"))
        tasks_modules = ["django_periodiq.setup"] # Broker module is first
        for conf in app_configs:
            module = conf.name + ".tasks"
            if module in ignored_modules:
                self.stdout.write(" * Ignored tasks module: %r" % module)
            else:
                self.stdout.write(" * Discovered tasks module: %r" % module)
                tasks_modules.append(module)

        return tasks_modules

    def _resolve_executable(self, exec_name):
        bin_dir = os.path.dirname(sys.executable)
        if bin_dir:
            return os.path.join(bin_dir, exec_name)
        return exec_name
